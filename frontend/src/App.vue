<script setup>
import { ref, onMounted } from 'vue'
import { getData } from './services/api'

const message = ref('Loading...')

onMounted(async () => {
  try {
    const data = await getData()
    message.value = data.message || 'Hello from API!'
  } catch (error) {
    message.value = 'Error loading data from API'
  }
})
</script>

<template>
  <div class="container">
    <h1>{{ message }}</h1>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}
</style>
