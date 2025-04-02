<template>
    <div class="form-container">
        <h1>Register</h1>
        <form @submit.prevent="handleRegister" class="auth-form">
            <input v-model="form.username" placeholder="Username" required>
            <input v-model="form.password" type="password" placeholder="Password" required>
            <input v-model="form.confirmPassword" type="password" placeholder="Confirm Password" required>
            <button type="submit">Register</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    username: '',
    password: '',
    confirmPassword: '',
})

const handleRegister = async () => {
    if (form.value.password !== form.value.confirmPassword) {
        alert('Passwords do not match!')
        return
    }

    try {
        const response = await api.post('register/', {
            username: form.value.username,
            password: form.value.password,
        })
        router.push('/login')
    } catch (error) {
        alert('Registering failed!')
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

