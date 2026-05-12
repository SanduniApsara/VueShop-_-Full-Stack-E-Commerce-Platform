<template>
  <footer style="background: #0f172a; color: #94a3b8;" class="pt-5 pb-4 mt-5">
    <div class="container">
      <div class="row g-4 mb-5">
        <!-- Brand -->
        <div class="col-lg-4">
          <h4 class="text-white fw-bold mb-3" style="font-family: 'Playfair Display', serif;">
            🛍️ Vue<span class="text-orange-400">Shop</span>
          </h4>
          <p class="mb-4">Your premier destination for quality products, delivered fast and hassle-free.</p>
          <div class="d-flex gap-3">
            <a href="#" class="social-btn">📘</a>
            <a href="#" class="social-btn">📸</a>
            <a href="#" class="social-btn">🐦</a>
          </div>
        </div>

        <!-- Quick links -->
        <div class="col-sm-6 col-lg-2">
          <h6 class="text-white fw-semibold mb-3 text-uppercase tracking-wide" style="font-size:.8rem">Shop</h6>
          <ul class="list-unstyled d-flex flex-column gap-2">
            <li><router-link to="/products" class="footer-link">All Products</router-link></li>
            <li><router-link to="/products?featured=true" class="footer-link">Featured</router-link></li>
            <li><router-link to="/products?in_stock=true" class="footer-link">In Stock</router-link></li>
          </ul>
        </div>

        <!-- Account -->
        <div class="col-sm-6 col-lg-2">
          <h6 class="text-white fw-semibold mb-3 text-uppercase tracking-wide" style="font-size:.8rem">Account</h6>
          <ul class="list-unstyled d-flex flex-column gap-2">
            <li><router-link to="/profile" class="footer-link">My Profile</router-link></li>
            <li><router-link to="/orders" class="footer-link">My Orders</router-link></li>
            <li><router-link to="/wishlist" class="footer-link">Wishlist</router-link></li>
          </ul>
        </div>

        <!-- Support -->
        <div class="col-lg-4">
          <h6 class="text-white fw-semibold mb-3 text-uppercase tracking-wide" style="font-size:.8rem">Stay Updated</h6>
          <p class="mb-3 text-sm">Subscribe for deals and new arrivals.</p>
          <div class="d-flex gap-2">
            <input type="email" placeholder="your@email.com" class="form-control form-control-sm rounded-pill border-0 bg-white bg-opacity-10 text-white" style="color: white !important;" />
            <button class="btn btn-sm rounded-pill text-white flex-shrink-0" style="background:#f97316; padding: 6px 16px;">Go</button>
          </div>
        </div>
      </div>

      <hr class="border-secondary" />
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 pt-3">
        <p class="mb-0 text-sm">© {{ new Date().getFullYear() }} VueShop. All rights reserved.</p>
        <div class="d-flex gap-4">
          <a href="#" class="footer-link text-sm">Privacy Policy</a>
          <a href="#" class="footer-link text-sm">Terms of Service</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-link { color: #94a3b8; text-decoration: none; font-size: .875rem; transition: color .2s; }
.footer-link:hover { color: #f97316; }
.social-btn {
  width: 36px; height: 36px; border-radius: 50%;
  background: rgba(255,255,255,.1); display: flex;
  align-items: center; justify-content: center;
  font-size: 1rem; cursor: pointer; transition: background .2s;
  text-decoration: none;
}
.social-btn:hover { background: #f97316; }
</style>
