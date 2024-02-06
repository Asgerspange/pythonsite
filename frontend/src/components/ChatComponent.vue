<template>
  <div class="container chat-container">
      <div v-for="(message, index) in messages" :key="index" :class="{ 'user-message': message.sender === 'user', 'bot-message': message.sender === 'bot' }">
          <p>{{ message.sender === 'user' ? 'You: ' : 'Bot: ' }}{{ message.content }}</p>
      </div>
      <div class="user-input">
          <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message here..." />
          <button @click="sendMessage">Send</button>
      </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
      data() {
          return {
              userMessage: '',
              messages: []
          };
      },
      methods: {
          async sendMessage() {
              const message = { sender: 'user', content: this.userMessage };
              this.messages.push(message);
              this.userMessage = '';
              try {
                  // Simulating a conversation with an API
                  const response = await axios.post(`http://192.168.87.139:5000/generate`, { message: message.content+'.' });
                  const botMessage = { sender: 'bot', content: response.data.response };
                  console.log(response.data)
                  this.messages.push(botMessage);
              } catch (error) {
                  console.error('Error sending message:', error);
              }
          }
      }
  };
</script>
<style>
  .chat-container {
      margin: 0 auto;
      border: 1px solid #ccc;
      min-height: 200px;
      border-radius: 10px;
      padding: 20px;
      background-color: #111111;
  }
  .user-message {
      text-align: right;
      margin-bottom: 10px;
      color: #fce9e9;
      font-size: 20px;
  }
  .bot-message {
      text-align: left;
      margin-bottom: 10px;
      color: #fce9e9;
      font-size: 20px;
  }
  .user-input {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 120px;
  }
  .user-input input {
      flex: 1;
      margin-right: 10px;
      padding: 8px;
      border-radius: 5px;
      border: 1px solid #ccc;
      background-color: #161616;
      color: #fce9e9;
  }
  .user-input button {
      padding: 8px 15px;
      border-radius: 5px;
      border: none;
      background-color: #007bff;
      color: #fff;
      cursor: pointer;
  }
</style>