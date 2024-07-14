<template>
  <div id="app">
    <h1>Ollama Chat</h1>
    <div class="model-selector">
      <label for="model-select">Select Model:</label>
      <select id="model-select" v-model="selectedModel">
        <option value="llava">Llava</option>
        <option value="llama3">Llama3</option>
      </select>
    </div>
    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="message.type">
          <pre>{{ message.text }}</pre>
        </div>
      </div>
      <div class="input-container" :class="{ 'disabled': isLoading }">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message..." :disabled="isLoading">
        <button @click="sendMessage" :disabled="isLoading">Send</button>
      </div>
    </div>
    <div v-if="isLoading" class="loader-overlay">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script>
import './assests/main.css';
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      userInput: '',
      messages: [],
      isLoading: false,
      selectedModel: 'llava'
    }
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '' || this.isLoading) return;

      this.isLoading = true;
      this.messages.push({ type: 'user', text: this.userInput });

      try {
        const response = await axios.post('http://localhost:11434/api/generate', {
          model: this.selectedModel,
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
      } finally {
        this.isLoading = false;
        this.userInput = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      container.scrollTop = container.scrollHeight;
    }
  }
}
</script>