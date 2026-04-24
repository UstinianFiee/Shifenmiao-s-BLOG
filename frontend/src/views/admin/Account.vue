<template>
  <div class="account-page">

    <!-- 关于页面内容 -->
    <div class="section-card card">
      <div class="section-header">
        <h3 class="section-title">关于页面</h3>
        <button class="btn btn-primary" @click="saveProfile">保存</button>
      </div>
      <div class="profile-body">
        <!-- 头像 -->
        <div class="avatar-col">
          <div class="avatar-wrap">
            <img v-if="profile.avatar" :src="profile.avatar" class="avatar-img" />
            <div v-else class="avatar-placeholder">{{ profile.nickname?.charAt(0) || 'A' }}</div>
          </div>
          <input type="file" accept="image/*" @change="uploadAvatar" class="file-input" id="avatar-upload" />
          <label for="avatar-upload" class="btn" style="margin-top:10px;cursor:pointer;font-size:13px">更换头像</label>
          <p v-if="avatarMsg" class="tip">{{ avatarMsg }}</p>
        </div>
        <!-- 信息 -->
        <div class="profile-fields">
          <div class="field-group">
            <label>昵称</label>
            <input v-model="profile.nickname" class="field-input" placeholder="昵称" />
          </div>
          <div class="field-group">
            <label>个人简介</label>
            <textarea v-model="profile.bio" class="field-input" rows="4" placeholder="介绍一下自己..."></textarea>
          </div>
        </div>
      </div>
      <p v-if="profileMsg" class="tip success">{{ profileMsg }}</p>
    </div>

    <!-- 修改用户名 -->
    <div class="section-card card">
      <div class="section-header">
        <h3 class="section-title">修改用户名</h3>
        <button class="btn btn-primary" @click="saveUsername">保存</button>
      </div>
      <div class="field-group">
        <label>新用户名</label>
        <input v-model="usernameForm.username" class="field-input" placeholder="新用户名" />
      </div>
      <p v-if="usernameMsg" class="tip" :class="{ success: !usernameErr }">{{ usernameMsg }}</p>
    </div>

    <!-- 修改密码 -->
    <div class="section-card card">
      <div class="section-header">
        <h3 class="section-title">修改密码</h3>
        <button class="btn btn-primary" @click="savePassword">保存</button>
      </div>
      <div class="pwd-fields">
        <div class="field-group">
          <label>原密码</label>
          <div class="pwd-wrap">
            <input v-model="pwdForm.old_password" :type="showOld ? 'text' : 'password'" class="field-input" placeholder="原密码" />
            <button type="button" class="eye-btn" @click="showOld = !showOld">
              <svg v-if="showOld" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </button>
          </div>
        </div>
        <div class="field-group">
          <label>新密码</label>
          <div class="pwd-wrap">
            <input v-model="pwdForm.new_password" :type="showNew ? 'text' : 'password'" class="field-input" placeholder="新密码（至少6位）" />
            <button type="button" class="eye-btn" @click="showNew = !showNew">
              <svg v-if="showNew" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </button>
          </div>
        </div>
      </div>
      <p v-if="pwdMsg" class="tip" :class="{ success: !pwdErr }">{{ pwdMsg }}</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'
import { useAuthStore } from '../../stores/auth'
import { useToast } from '../../stores/toast'

const auth = useAuthStore()
const { show: toast } = useToast()

// profile
const profile = ref({ nickname: '', bio: '', avatar: '' })
const profileMsg = ref('')
const avatarMsg = ref('')

async function loadProfile() {
  const res = await api.get('/account/profile')
  profile.value = res.data
}

async function saveProfile() {
  await api.put('/account/profile', profile.value)
  toast('保存成功')
}

async function uploadAvatar(e) {
  const file = e.target.files[0]
  if (!file) return
  const fd = new FormData()
  fd.append('file', file)
  const res = await api.post('/upload', fd)
  profile.value.avatar = res.data.url
  avatarMsg.value = '上传成功，记得点保存'
}

// username
const usernameForm = ref({ username: '' })
const usernameMsg = ref('')
const usernameErr = ref(false)

async function saveUsername() {
  usernameErr.value = false
  try {
    const res = await api.put('/account/username', usernameForm.value)
    auth.username = res.data.username
    localStorage.setItem('username', res.data.username)
    toast('用户名修改成功')
    usernameForm.value.username = ''
  } catch (e) {
    usernameErr.value = true
    toast(e.response?.data?.msg || '修改失败', 'error')
  }
}

// password
const pwdForm = ref({ old_password: '', new_password: '' })
const pwdMsg = ref('')
const pwdErr = ref(false)
const showOld = ref(false)
const showNew = ref(false)

async function savePassword() {
  pwdErr.value = false
  try {
    await api.put('/account/password', pwdForm.value)
    toast('密码修改成功')
    pwdForm.value = { old_password: '', new_password: '' }
  } catch (e) {
    pwdErr.value = true
    toast(e.response?.data?.msg || '修改失败', 'error')
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.account-page { display: flex; flex-direction: column; gap: 20px; }
.section-card { padding: 24px; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.section-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }

.profile-body { display: flex; gap: 32px; align-items: flex-start; }
.avatar-col { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.avatar-wrap { width: 90px; height: 90px; border-radius: 50%; overflow: hidden; border: 2px solid var(--border); }
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, var(--accent), var(--accent-2)); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 700; color: #fff; }
.file-input { display: none; }

.profile-fields { flex: 1; display: flex; flex-direction: column; gap: 16px; }
.pwd-fields { display: flex; gap: 20px; flex-wrap: wrap; }
.pwd-fields .field-group { flex: 1; min-width: 200px; }

@media (max-width: 768px) {
  .profile-body { flex-direction: column; }
  .section-header { flex-wrap: wrap; gap: 10px; }
}

.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-group label { font-size: 13px; color: var(--text-secondary); }
.field-input {
  width: 100%; padding: 10px 14px;
  background: var(--bg-primary); border: 1px solid var(--border);
  border-radius: var(--radius); color: var(--text-primary); font-size: 14px;
  outline: none; transition: border-color 0.3s; resize: vertical;
}
.field-input:focus { border-color: var(--accent); }

.pwd-wrap { position: relative; }
.pwd-wrap .field-input { padding-right: 40px; }
.eye-btn { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; display: flex; align-items: center; transition: color 0.2s; }
.eye-btn:hover { color: var(--accent); }

.tip { font-size: 13px; color: #ef4444; margin-top: 12px; }
.tip.success { color: var(--accent); }
</style>
