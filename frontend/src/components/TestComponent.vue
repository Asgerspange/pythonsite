<template>
    <div class="container chat-container">
      <!-- Message display area -->
      <div v-for="(message, index) in messages" :key="index" :class="{ 'user-message': message.sender === 'user', 'bot-message': message.sender === 'bot' }">
        <p>{{ message.sender === 'user' ? 'You: ' : 'Sebastian: ' }}{{ message.content }}</p>
      </div>
  
      <!-- User input area -->
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
        userMessage: '', // User's message input
        messages: [],    // Array to store chat messages
      };
    },
    methods: {
      async sendMessage() {
        // Prepare message object
        const message = {
          prompt: this.userMessage,
          context: 'Sebastian is a compassionate and empathetic individual who deeply cares about the well-being of others. He strives to understand and support those around him, always ready to lend a helping hand or offer a listening ear.',
        };
  
        // Add user's message to chat display
        this.messages.push({ sender: 'user', content: this.userMessage });
        this.userMessage = ''; // Clear user's input field
  
        try {
          // Send message to backend
          const response = await axios.get('http://localhost:5000/get_chatbot_response/', { params: message });
  
          // Display bot's response
          const botMessage = { sender: 'bot', content: response.data.response };
          this.messages.push(botMessage);
        } catch (error) {
          console.error('Error sending message:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styles for the chat interface */
  .chat-container {
    margin: 0 auto;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 20px;
    background-color: #f9f9f9;
  }
  
  .user-message {
    text-align: right;
    margin-bottom: 10px;
  }
  
  .bot-message {
    text-align: left;
    margin-bottom: 10px;
  }
  
  .user-input {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
  }
  
  .user-input input {
    flex: 1;
    margin-right: 10px;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
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
  