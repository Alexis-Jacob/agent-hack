<template>
  <div class="page-container">
    <div class="chat-container">
      <!-- Input Section (Top Center) -->
      <div class="chat-input-container">
        <div class="chat-input-wrapper">
          <input 
            v-model="message"
            @keyup.enter="sendMessage"
            placeholder="Type your message..."
            :disabled="isLoading"
          />
          <button 
            @click="startNewChat"
            class="new-chat-btn"
          >
            New Chat
          </button>
          <button 
            @click="sendMessage"
            :disabled="isLoading || !message.trim()"
          >
            {{ isLoading ? 'Sending...' : 'Send' }}
          </button>
        </div>
      </div>

      <!-- Message List Section -->
      <div class="chat-messages">
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          class="chat-message"
          :class="{ 'user-message': msg.startsWith('You:'), 'bot-message': msg.startsWith('Bot:') }"
        >
          <div v-if="msg.startsWith('You:')" class="message-content">
            {{ msg.replace('You:', '').trim() }}
          </div>
          <div v-else class="message-content markdown-body" v-html="renderMarkdown(msg.replace('Bot:', '').trim())"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const message = ref('')
const isLoading = ref(false)
const messages = ref([])

const renderMarkdown = (text) => {
  // Configure marked options
  marked.setOptions({
    breaks: true, // Enable line breaks
    gfm: true,    // Enable GitHub Flavored Markdown
    headerIds: false, // Disable header IDs for security
    mangle: false,    // Disable mangling for security
  })
  
  // Convert markdown to HTML and sanitize it
  const html = marked(text)
  return DOMPurify.sanitize(html)
}

const startNewChat = async () => {
  try {
    await axios.post('http://localhost:8000/api/new_chat')
    messages.value = []
  } catch (error) {
    console.error('Error starting new chat:', error)
  }
}

const sendMessage = async () => {
  const trimmed = message.value.trim()
  if (!trimmed) return

  isLoading.value = true
  try {
    const response = await axios.post('http://localhost:8000/api/chat', {
      message: trimmed
    })

    // Add user message + response to the messages list
    messages.value.push(`You: ${trimmed}`)
    messages.value.push(`Bot: ${response.data?.message || 'No response'}`)

    message.value = ''
  } catch (error) {
    console.error('Error sending message:', error)
    messages.value.push('Bot: [Error sending message]')
  } finally {
    isLoading.value = false
  }
}
</script>

<style>
@import 'github-markdown-css/github-markdown.css';

.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #F9FAFB;
  padding-top: 2rem;
}

.chat-container {
  width: 75vh;
  max-width: 100%;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.chat-input-container {
  padding: 1rem 2rem;
  border-bottom: 1px solid #E5E7EB;
  background: #ffffff;
}

.chat-input-wrapper {
  display: flex;
  gap: 0.5rem;
  background: #F9FAFB;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #E5E7EB;
}

.chat-messages {
  padding: 1rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  max-height: 60vh;
}

.chat-message {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
}

.user-message {
  background: #F3F4F6;
  color: #1D2939;
  align-self: flex-end;
  max-width: 80%;
}

.bot-message {
  background: #F0F9FF;
  color: #1D2939;
  align-self: flex-start;
  max-width: 80%;
}

.message-content {
  word-break: break-word;
}

.markdown-body {
  background: transparent !important;
  font-size: 0.95rem !important;
}

.markdown-body pre {
  background: #1F2937;
  color: #F9FAFB;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
}

.markdown-body code {
  background: #F3F4F6;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

.markdown-body pre code {
  background: transparent;
  padding: 0;
  color: inherit;
}

input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  font-size: 1rem;
  background: #ffffff;
  transition: all 0.2s ease;
  color: #1D2939;
}

input:focus {
  outline: none;
  border-color: #2563EB;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

button {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #2563EB;
  color: white;
}

button:hover:not(:disabled) {
  background: #1D4ED8;
}

button:disabled {
  background: #93C5FD;
  cursor: not-allowed;
}

.new-chat-btn {
  background: #E5E7EB;
  color: #4B5563;
}

.new-chat-btn:hover:not(:disabled) {
  background: #D1D5DB;
}
</style>
