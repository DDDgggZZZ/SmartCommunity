<template>
  <router-view />
</template>

<style>
/* 全局滚动条样式，适配极客风 */
/* 让滚动条变细，颜色变暗，符合黑客终端的审美 */

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--geek-bg); /* 对应 geek-theme.css 中的背景色 */
}

::-webkit-scrollbar-thumb {
  background: var(--geek-border);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--geek-primary); /* 悬停时显示高亮色 */
}
</style>