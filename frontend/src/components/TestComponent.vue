<template>
    <div class="container">
      <div v-for="(message, index) in messages" :key="index" :class="{ 'user-message': message.sender === 'user', 'bot-message': message.sender === 'bot' }">
        {{ message.content }}
      </div>
      <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message here..." />
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
          const response = await axios.get(`http://localhost:5000/get_response/${encodeURIComponent(message.content)}`);
          const botMessage = { sender: 'bot', content: response.data.response };
          this.messages.push(botMessage);
        } catch (error) {
          console.error('Error sending message:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  .user-message {
    text-align: right;
    margin-bottom: 5px;
  }
  
  .bot-message {
    text-align: left;
    margin-bottom: 5px;
  }
  </style>
  