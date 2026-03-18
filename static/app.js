// Claude Code Model Switch - Frontend Logic (Multi-Provider)

let providers = [];
let currentProviderId = null;
let currentModelId = null;

const providersContainer = document.getElementById('providers-container');
const modelSection = document.getElementById('model-section');
const modelsContainer = document.getElementById('models-container');
const currentProviderEl = document.getElementById('current-provider');
const currentModelEl = document.getElementById('current-model');
const statusMessage = document.getElementById('status-message');
const configPathEl = document.getElementById('config-path');

// 初始化
document.addEventListener('DOMContentLoaded', init);

async function init() {
    await loadProviders();
    await loadCurrentConfig();
    await loadConfigStatus();
}

async function loadProviders() {
    try {
        const response = await fetch('/api/providers');
        const data = await response.json();
        providers = data.providers;
        renderProviders();
    } catch (error) {
        providersContainer.innerHTML = `<span class="error">加载供应商失败: ${error.message}</span>`;
    }
}

async function loadCurrentConfig() {
    try {
        const response = await fetch('/api/current');
        const data = await response.json();

        if (response.status === 404) {
            currentProviderEl.textContent = '未配置';
            currentModelEl.textContent = '未配置';
            return;
        }

        currentProviderId = data.provider_id || 'unknown';
        currentModelId = data.model_id || 'unknown';

        // 显示当前配置
        const provider = providers.find(p => p.id === currentProviderId);
        currentProviderEl.textContent = provider ? provider.name : currentProviderId;
        currentModelEl.textContent = currentModelId;

        // 更新选中状态
        updateProviderSelectedState();
        if (provider) {
            renderModels(provider);
        }
    } catch (error) {
        console.error('Load config error:', error);
    }
}

async function loadConfigStatus() {
    try {
        const response = await fetch('/api/config_status');
        const data = await response.json();

        if (data.config_path) {
            configPathEl.textContent = data.config_path;
        }
    } catch (error) {
        console.error('Config status error:', error);
    }
}

function renderProviders() {
    if (providers.length === 0) {
        providersContainer.innerHTML = '<span class="loading">暂无可用供应商</span>';
        return;
    }

    providersContainer.innerHTML = providers.map(provider => `
        <div class="provider-card ${provider.id === currentProviderId ? 'selected' : ''}"
             data-provider-id="${provider.id}">
            <div class="provider-name">${provider.name}</div>
            <div class="provider-models-count">${provider.models.length} 个模型</div>
        </div>
    `).join('');

    // 点击供应商显示模型
    providersContainer.querySelectorAll('.provider-card').forEach(card => {
        card.addEventListener('click', () => {
            const providerId = card.dataset.providerId;
            selectProvider(providerId);
        });
    });
}

function selectProvider(providerId) {
    // 更新选中状态
    providersContainer.querySelectorAll('.provider-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.providerId === providerId);
    });

    // 找到供应商并渲染模型
    const provider = providers.find(p => p.id === providerId);
    if (provider) {
        renderModels(provider);
    }
}

function renderModels(provider) {
    modelSection.style.display = 'block';

    if (provider.models.length === 0) {
        modelsContainer.innerHTML = '<span class="loading">该供应商暂无模型</span>';
        return;
    }

    modelsContainer.innerHTML = provider.models.map(model => `
        <div class="model-card ${model.id === currentModelId ? 'selected' : ''}"
             data-model-id="${model.id}">
            <div class="model-name">${model.name}</div>
            <div class="model-id">${model.id}</div>
            <div class="model-desc">${model.description || ''}</div>
            <button class="switch-btn"
                    onclick="switchTo('${provider.id}', '${model.id}')"
                    ${model.id === currentModelId ? 'disabled' : ''}>
                ${model.id === currentModelId ? '当前使用' : '切换'}
            </button>
        </div>
    `).join('');
}

function updateProviderSelectedState() {
    providersContainer.querySelectorAll('.provider-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.providerId === currentProviderId);
    });
}

async function switchTo(providerId, modelId) {
    showStatus('', '');

    // 禁用所有按钮
    document.querySelectorAll('.switch-btn').forEach(btn => btn.disabled = true);

    try {
        const response = await fetch('/api/switch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                provider_id: providerId,
                model_id: modelId
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '切换失败');
        }

        // 切换成功
        currentProviderId = providerId;
        currentModelId = modelId;

        const provider = providers.find(p => p.id === providerId);
        currentProviderEl.textContent = provider ? provider.name : providerId;
        currentModelEl.textContent = modelId;

        showStatus(data.message || `已切换到 ${provider?.name || providerId}/${modelId}`, 'success');

        // 更新选中状态
        updateProviderSelectedState();
        if (provider) {
            renderModels(provider);
        }

    } catch (error) {
        showStatus(error.message, 'error');
    } finally {
        // 恢复按钮状态
        document.querySelectorAll('.switch-btn').forEach(btn => {
            const card = btn.closest('.model-card');
            if (card.dataset.modelId !== currentModelId) {
                btn.disabled = false;
            }
        });
    }
}

function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = 'status-message ' + type;

    if (type === 'success') {
        setTimeout(() => {
            statusMessage.textContent = '';
            statusMessage.className = 'status-message';
        }, 3000);
    }
}