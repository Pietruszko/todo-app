<template>
    <div class="form-container">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin" class="auth-form">
            <input v-model="form.username" placeholder="Username" required>
            <input v-model="form.password" type="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { ref } from 'vue'
import api from '@/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    username: '',
    password: ''
})

onMounted(() => {
    if (localStorage.getItem('token')) {
    router.push('/tasks')
    }
})

const handleLogin = async () => {
    try {
        const response = await api.post('login/', form.value)
        localStorage.setItem('token', response.data.access)
        router.push('/tasks')
    } catch (error) {
        alert('Login failed!')
    }
}
</script>

<style scoped>
.form-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
}
input {
    display: block;
    width: 100%;
    margin: 0.5rem 0;
    padding: 0.5rem;
}
button {
    background: #42b983;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>

