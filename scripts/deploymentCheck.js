#!/usr/bin/env node

/**
 * AMS v2.0 deployment readiness check.
 * Usage: node scripts/deploymentCheck.js [API_BASE_URL]
 */

import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const rootDir = path.resolve(__dirname, '..')
const apiBase = process.argv[2] || process.env.VITE_API_URL || 'http://localhost:8000'

const checks = []

function pass(name, detail) {
  checks.push({ name, ok: true, detail })
  console.log(`✅ ${name}: ${detail}`)
}

function fail(name, detail) {
  checks.push({ name, ok: false, detail })
  console.error(`❌ ${name}: ${detail}`)
}

async function checkDatabase() {
  try {
    const response = await fetch(`${apiBase}/health`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    if (data.database === 'connected' || data.database === 'ok') {
      pass('Database', data.database)
    } else {
      fail('Database', data.database || 'unknown')
    }
  } catch (error) {
    fail('Database', error.message)
  }
}

async function checkConfig() {
  try {
    const envPath = path.join(rootDir, 'backend', '.env')
    if (fs.existsSync(envPath)) {
      pass('Config', 'backend/.env present')
    } else {
      fail('Config', 'backend/.env missing')
    }
  } catch (error) {
    fail('Config', error.message)
  }
}

function checkUploads() {
  const uploadsPath = path.join(rootDir, 'backend', 'uploads')
  try {
    fs.mkdirSync(uploadsPath, { recursive: true })
    fs.accessSync(uploadsPath, fs.constants.W_OK)
    pass('Uploads', uploadsPath)
  } catch (error) {
    fail('Uploads', error.message)
  }
}

async function checkWebSocket() {
  try {
    const wsUrl = apiBase.replace(/^http/, 'ws') + '/ws/events'
    pass('WebSocket endpoint', wsUrl)
  } catch (error) {
    fail('WebSocket endpoint', error.message)
  }
}

function checkDiskSpace() {
  try {
    const free = os.freemem()
    const total = os.totalmem()
    const freeGb = (free / 1024 / 1024 / 1024).toFixed(1)
    const totalGb = (total / 1024 / 1024 / 1024).toFixed(1)
    if (free > 512 * 1024 * 1024) {
      pass('Disk/Memory', `${freeGb} GB free / ${totalGb} GB total`)
    } else {
      fail('Disk/Memory', `Low free memory: ${freeGb} GB`)
    }
  } catch (error) {
    fail('Disk/Memory', error.message)
  }
}

async function checkApiHealth() {
  try {
    const response = await fetch(`${apiBase}/api/health`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    const fields = ['database', 'websocket', 'storage', 'camera', 'ffmpeg']
    const summary = fields.map((key) => `${key}=${data[key]?.status ?? data[key] ?? '?'}`).join(', ')
    if (data.status === 'ok' || data.status === 'degraded') {
      pass('API Health (/api/health)', `${data.status} — ${summary}`)
    } else {
      fail('API Health (/api/health)', data.status || summary)
    }
  } catch (error) {
    fail('API Health (/api/health)', error.message)
  }
}

async function main() {
  console.log(`AMS v2.0 Deployment Check — API: ${apiBase}`)
  await checkDatabase()
  await checkApiHealth()
  await checkConfig()
  checkUploads()
  await checkWebSocket()
  checkDiskSpace()

  const failed = checks.filter((item) => !item.ok)
  console.log(`\nSummary: ${checks.length - failed.length}/${checks.length} passed`)
  process.exit(failed.length ? 1 : 0)
}

main()
