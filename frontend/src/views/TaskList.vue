<template>
    <div class="task-manager">
        <h1>Tasks:</h1>

        <form @submit.prevent="handleAddTask" class="task-form">
            <input v-model="newTask.title" placeholder="New task title" required>
            <button type="submit">Add Task</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>

        <div v-if="loading">Loading...</div>
        <ul v-else>
            <li v-for="task in tasks" :key="task.id" class="task-item">
                <span
                    class="checkbox"
                    @click="toggleTaskCompletion(task)"
                    :class="{ checked: task.completed }"
                >
                    {{ task.completed ? '[x]' : '[ ]' }}
                </span>
                <input
                    v-if="editedTask && task.id === editedTask.id"
                    v-model="editedTask.title"
                    @blur="saveTaskEdit(task)"
                    @keyup.enter="saveTaskEdit(task)"
                    @keyup.escape="editedTask = null"
                    class="title-edit"
                    v-focus
                >
                <span
                    v-else
                    @dblclick="startEditing(task)"
                    class="task-title"
                    :class="{ completed: task.completed}"
                >
                    {{ task.title }}
                </span>
                <button @click="deleteTask(task.id)">Delete</button>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/auth.js'

const loading = ref(true)
const tasks = ref([])
const errorMessage = ref('')
const newTask = ref({ title: '' })
const editedTask = ref(null)
const vFocus = {
  mounted: (el) => el.focus()
}

function startEditing(task) {
    editedTask.value = { ...task}
}

onMounted(fetchTasks)

async function fetchTasks() {
    try {
        const response = await api.get('tasks/')
        tasks.value = response.data
    } catch (error) {
        console.error('Failed to fetch tasks:', error)
    } finally {
        loading.value = false
    }
}

async function handleAddTask() {
    if (!newTask.value.title.trim()) {
        errorMessage.value = 'Title cannot be empty!'
        return
    }

    try {
        const response = await api.post('tasks/', {
            title: newTask.value.title
        })
        tasks.value.push(response.data)
        newTask.value.title = ''
        errorMessage.value = ''
    } catch (error) {
        errorMessage.value = error.response?.data?.title?.[0] || 'Failed to add task'
    }
}

async function deleteTask(taskId) {
    try {
        await api.delete(`tasks/${taskId}/`)
        tasks.value = tasks.value.filter(t => t.id !== taskId)
    } catch (error) {
        console.error('Failed to delete task:', error)
    }
}

async function saveTaskEdit(originalTask) {
    try {
        const response = await api.patch(`tasks/${originalTask.id}/`, {
            title: editedTask.value.title
        })
        Object.assign(originalTask, response.data)
        editedTask.value = null
    } catch (error) {
        console.error('Update failed:', error)
    } 
}

async function toggleTaskCompletion(task) {
    try {
        const response = await api.patch(`tasks/${task.id}/`, {
            completed: !task.completed
        })
        task.completed = response.data.completed
    } catch (error) {
        console.error('Failed to toggle task completion:', error)
    }
}
</script>

<style scoped>
ul {
    list-style: none;
    padding: 0;
}
li {
    margin: 8px 0;
    padding: 8px;
    border: 1px solid #eee;
}
.error {
    color: red;
}
.task-manager {
    max-width: 600px;
    margin:0 auto;
}
.task-form {
    margin-bottom: 1rem;
}
.checkbox {
    cursor: pointer;
    user-select: none;
    margin-right: 8px;
    font-family: monospace;
}
.checkbox.checked {
    color: #42b983
}
.task-title.completed {
    text-decoration: line-through;
    opacity: 0.8;
}
.task-item {
  display: flex;
  align-items: center;
  padding: 8px;
  margin: 8px 0;
  border: 1px solid #eee;
}
.task-title {
  flex-grow: 1; 
}
.title-edit {
  flex-grow: 1;
  padding: 0 4px;
  margin: 0 8px;
}
.task-title, .title-edit {
  width: 0;
}
</style>