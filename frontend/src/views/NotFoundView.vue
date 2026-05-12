<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center text-center">
    <div>
      <div style="font-size: 6rem;">🔍</div>
      <h1 class="display-1 fw-bold text-orange-500">404</h1>
      <h3 class="fw-bold mb-3">Page Not Found</h3>
      <p class="text-muted mb-5">The page you're looking for doesn't exist or has been moved.</p>
      <div class="d-flex gap-3 justify-content-center">
        <router-link to="/" class="btn-shop">Go Home</router-link>
        <router-link to="/products" class="btn-outline-shop">Browse Products</router-link>
      </div>
    </div>
  </div>
</template>
