document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = 'http://localhost:5001';
    const board = document.getElementById('board');
    const status = document.getElementById('status');
    const resetBtn = document.getElementById('reset');
    const themeBtn = document.getElementById('theme-toggle');
    const difficultySelect = document.getElementById('difficulty');

    // Initialize empty board
    function initializeBoard() {
        board.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.index = i;
            board.appendChild(cell);
        }
    }

    // Theme management
    function initTheme() {
        const darkMode = localStorage.getItem('darkMode') === 'true';
        document.body.classList.toggle('dark-mode', darkMode);
        updateThemeButton();
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        updateThemeButton();
    }

    function updateThemeButton() {
        const isDark = document.body.classList.contains('dark-mode');
        themeBtn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
    }

    // Stats handling with defaults
    function updateStats(stats = {}) {
        const defaults = { wins: 0, losses: 0, draws: 0 };
        const currentStats = { ...defaults, ...stats };
        
        document.getElementById('wins').textContent = currentStats.wins;
        document.getElementById('losses').textContent = currentStats.losses;
        document.getElementById('draws').textContent = currentStats.draws;
    }

    // Safe API calls
    async function safeFetch(endpoint, options = {}) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...(options.headers || {})
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Request failed');
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            status.textContent = `Error: ${error.message}`;
            throw error;
        }
    }

    // Update board display
    function updateBoard(boardState = Array(9).fill(' ')) {
        document.querySelectorAll('.cell').forEach((cell, i) => {
            cell.textContent = boardState[i] || ' ';
            cell.className = 'cell';
            if (boardState[i] === 'X') cell.classList.add('x');
            if (boardState[i] === 'O') cell.classList.add('o');
        });
    }

    // Handle cell clicks
    async function handleCellClick(e) {
        if (!e.target.classList.contains('cell')) return;
        
        try {
            const index = parseInt(e.target.dataset.index);
            const data = await safeFetch('/move', {
                method: 'POST',
                body: JSON.stringify({ position: index })
            });
            
            updateBoard(data.board);
            
            if (data.gameOver) {
                status.textContent = data.winner 
                    ? `Player ${data.winner} wins!` 
                    : "Game ended in a draw!";
                updateStats(data.stats);
            } else {
                status.textContent = 'Your turn (X)';
                updateStats(data.stats);
            }
        } catch (error) {
            console.error('Move error:', error);
            updateStats();
        }
    }

    // Reset game
    async function initGame() {
        try {
            initializeBoard();
            const difficulty = difficultySelect.value;
            const data = await safeFetch('/reset', {
                method: 'POST',
                body: JSON.stringify({ difficulty })
            });
            updateBoard(data.board);
            updateStats(data.stats);
            status.textContent = `Your turn (X) - ${difficulty} mode`;
        } catch (error) {
            console.error('Init error:', error);
            updateStats();
        }
    }

    // Initialize game
    initializeBoard();
    initTheme();
    initGame();

    // Event listeners
    board.addEventListener('click', handleCellClick);
    resetBtn.addEventListener('click', initGame);
    themeBtn.addEventListener('click', toggleTheme);
});