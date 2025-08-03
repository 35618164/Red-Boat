// 主要JavaScript功能
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask团队项目已加载');
    
    // API测试功能
    const testApiButton = document.getElementById('test-api');
    const apiResultDiv = document.getElementById('api-result');
    
    if (testApiButton && apiResultDiv) {
        testApiButton.addEventListener('click', function() {
            testApiButton.disabled = true;
            testApiButton.textContent = '测试中...';
            apiResultDiv.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> 正在请求API...';
            
            // 调用API
            fetch('/api/hello')
                .then(response => response.json())
                .then(data => {
                    apiResultDiv.innerHTML = `
                        <h5>API响应结果：</h5>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    `;
                })
                .catch(error => {
                    apiResultDiv.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>错误：</strong> ${error.message}
                        </div>
                    `;
                })
                .finally(() => {
                    testApiButton.disabled = false;
                    testApiButton.textContent = '测试API接口';
                });
        });
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 导航栏活动状态
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});

// 实用工具函数
const Utils = {
    // 显示消息提示
    showAlert: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            // 3秒后自动消失
            setTimeout(() => {
                alertDiv.remove();
            }, 3000);
        }
    },
    
    // 格式化时间
    formatDateTime: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
};
