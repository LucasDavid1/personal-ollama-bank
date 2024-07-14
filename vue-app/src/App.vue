<template>
  <div id="app">
    <h1>Ollama Chat</h1>
    <div class="chat-container">
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" :class="message.type">
          <pre>{{ message.text }}</pre>
        </div>
      </div>
      <div class="input-container">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message...">
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      userInput: '',
      messages: []
    }
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '') return;

      this.messages.push({ type: 'user', text: this.userInput });

      try {
        const response = await axios.post('http://localhost:11434/api/generate', {
          model: "llava",
          prompt: this.userInput
        }, {
          responseType: 'text',
          transformResponse: (data) => data
        });

        let fullResponse = '';
        const lines = response.data.split('\n');
        for (const line of lines) {
          if (line.trim() !== '') {
            try {
              const jsonResponse = JSON.parse(line);
              if (jsonResponse.response) {
                fullResponse += jsonResponse.response;
              }
            } catch (parseError) {
              console.error('Error parsing JSON:', parseError);
            }
          }
        }

        this.messages.push({ type: 'bot', text: fullResponse.trim() });

      } catch (error) {
        console.error('Error:', error);
        this.messages.push({ type: 'error', text: 'An error occurred while fetching the response.' });
      }

      this.userInput = '';
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.chat-container {
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 20px;
}

.messages {
  height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
  text-align: left;
}

.user, .bot, .error {
  margin: 10px 0;
  padding: 10px;
  border-radius: 4px;
}

.user {
  background-color: #e6f3ff;
}

.bot {
  background-color: #f0f0f0;
}

.error {
  background-color: #ffe6e6;
}

.input-container {
  display: flex;
}

input {
  flex-grow: 1;
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
</style>