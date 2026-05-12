<template>
  <div class="container py-5" style="max-width: 960px;">
    <h2 class="fw-bold mb-5">Checkout</h2>

    <!-- Steps indicator -->
    <div class="d-flex align-items-center mb-5">
      <div v-for="(step, i) in steps" :key="i" class="d-flex align-items-center flex-grow-1">
        <div :class="['step-circle', currentStep >= i + 1 ? 'done' : 'pending']">
          <span v-if="currentStep > i + 1">✓</span>
          <span v-else>{{ i + 1 }}</span>
        </div>
        <span :class="['step-label ms-2', currentStep === i + 1 ? 'fw-semibold text-dark' : 'text-muted']">{{ step }}</span>
        <div v-if="i < steps.length - 1" class="flex-grow-1 border-top mx-3" style="border-color: #e2e8f0!important;"></div>
      </div>
    </div>

    <div class="row g-5">
      <!-- Left: Form area -->
      <div class="col-lg-7">
        <!-- Step 1: Shipping address -->
        <div v-if="currentStep === 1">
          <h5 class="fw-bold mb-4">Shipping Address</h5>
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-medium">Full Name</label>
              <input v-model="form.shipping_name" class="input-shop" placeholder="John Doe" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-medium">Phone</label>
              <input v-model="form.shipping_phone" class="input-shop" placeholder="+1 555 000 0000" />
            </div>
            <div class="col-12">
              <label class="form-label fw-medium">Street Address</label>
              <input v-model="form.shipping_street" class="input-shop" placeholder="123 Main St" />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-medium">City</label>
              <input v-model="form.shipping_city" class="input-shop" placeholder="New York" />
            </div>
            <div class="col-md-3">
              <label class="form-label fw-medium">State</label>
              <input v-model="form.shipping_state" class="input-shop" placeholder="NY" />
            </div>
            <div class="col-md-3">
              <label class="form-label fw-medium">ZIP</label>
              <input v-model="form.shipping_postal_code" class="input-shop" placeholder="10001" />
            </div>
          </div>
        </div>

        <!-- Step 2: Shipping method -->
        <div v-if="currentStep === 2">
          <h5 class="fw-bold mb-4">Shipping Method</h5>
          <div class="d-flex flex-column gap-3">
            <label
              v-for="method in shippingMethods"
              :key="method.id"
              :class="['shipping-option', form.shipping_method === method.id && 'selected']"
            >
              <input type="radio" :value="method.id" v-model="form.shipping_method" class="d-none" />
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="fw-semibold">{{ method.name }}</div>
                  <div class="text-sm text-muted">{{ method.eta }}</div>
                </div>
                <span class="fw-bold text-orange-500">${{ method.price }}</span>
              </div>
            </label>
          </div>
        </div>

        <!-- Step 3: Payment -->
        <div v-if="currentStep === 3">
          <h5 class="fw-bold mb-4">Payment</h5>
          <div class="border rounded-3 p-4 bg-gray-50 text-center">
            <p class="text-muted mb-3">💳 Secure payment powered by Stripe</p>
            <div class="row g-3">
              <div class="col-12">
                <label class="form-label fw-medium text-start d-block">Card Number</label>
                <input class="input-shop" placeholder="4242 4242 4242 4242" />
              </div>
              <div class="col-md-6">
                <label class="form-label fw-medium text-start d-block">Expiry</label>
                <input class="input-shop" placeholder="MM / YY" />
              </div>
              <div class="col-md-6">
                <label class="form-label fw-medium text-start d-block">CVC</label>
                <input class="input-shop" placeholder="123" />
              </div>
            </div>
            <p class="text-xs text-muted mt-3">🔒 Your card details are encrypted and never stored</p>
          </div>
        </div>

        <!-- Navigation buttons -->
        <div class="d-flex justify-content-between mt-5">
          <button v-if="currentStep > 1" @click="currentStep--" class="btn btn-outline-secondary rounded-pill px-4">
            ← Back
          </button>
          <div v-else></div>
          <button
            v-if="currentStep < 3"
            @click="nextStep"
            class="btn-shop"
          >
            Continue →
          </button>
          <button
            v-else
            @click="placeOrder"
            :disabled="placing"
            class="btn-shop px-8"
          >
            {{ placing ? 'Placing Order...' : '✅ Place Order' }}
          </button>
        </div>
      </div>

      <!-- Right: Order summary -->
      <div class="col-lg-5">
        <div class="card border-0 shadow-sm rounded-3 p-4 sticky-top" style="top: 80px;">
          <h6 class="fw-bold mb-4">Order Summary</h6>

          <div class="d-flex flex-column gap-3 mb-4">
            <div v-for="item in cartStore.items" :key="item.id" class="d-flex gap-3 align-items-start">
              <img :src="item.product.image" class="rounded-2 object-fit-cover flex-shrink-0" style="width:52px;height:52px;" />
              <div class="flex-grow-1">
                <p class="text-sm fw-medium mb-0">{{ item.product.name }}</p>
                <p class="text-muted text-xs mb-0">Qty: {{ item.quantity }}</p>
              </div>
              <span class="fw-semibold text-sm">${{ Number(item.line_total).toFixed(2) }}</span>
            </div>
          </div>

          <hr />
          <div class="d-flex flex-column gap-2 text-sm">
            <div class="d-flex justify-content-between">
              <span class="text-muted">Subtotal</span>
              <span>${{ Number(cartStore.subtotal).toFixed(2) }}</span>
            </div>
            <div class="d-flex justify-content-between">
              <span class="text-muted">Shipping</span>
              <span>${{ selectedShipping.price }}</span>
            </div>
            <div class="d-flex justify-content-between">
              <span class="text-muted">Tax (8%)</span>
              <span>${{ (cartStore.subtotal * 0.08).toFixed(2) }}</span>
            </div>
          </div>
          <hr />
          <div class="d-flex justify-content-between fw-bold fs-5">
            <span>Total</span>
            <span class="text-orange-500">${{ orderTotal }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/store/modules/cart'
import api from '@/utils/api'

const router = useRouter()
const cartStore = useCartStore()

const currentStep = ref(1)
const placing = ref(false)
const steps = ['Address', 'Shipping', 'Payment']

const shippingMethods = [
  { id: 'standard', name: 'Standard Shipping', eta: '5–7 business days', price: '5.99' },
  { id: 'express', name: 'Express Shipping', eta: '2–3 business days', price: '12.99' },
  { id: 'overnight', name: 'Overnight Shipping', eta: '1 business day', price: '24.99' },
]

const form = ref({
  shipping_name: '',
  shipping_phone: '',
  shipping_street: '',
  shipping_city: '',
  shipping_state: '',
  shipping_postal_code: '',
  shipping_country: 'US',
  shipping_method: 'standard',
})

const selectedShipping = computed(() =>
  shippingMethods.find(m => m.id === form.value.shipping_method) || shippingMethods[0]
)

const orderTotal = computed(() => {
  const sub = Number(cartStore.subtotal)
  const ship = Number(selectedShipping.value.price)
  const tax = sub * 0.08
  return (sub + ship + tax).toFixed(2)
})

function nextStep() {
  if (currentStep.value < 3) currentStep.value++
}

async function placeOrder() {
  placing.value = true
  try {
    const { data } = await api.post('/orders/create/', form.value)
    await cartStore.fetchCart()
    router.push(`/orders/${data.id}`)
  } catch (e) {
    alert('Failed to place order. Please try again.')
  } finally {
    placing.value = false
  }
}
</script>

<style scoped>
.step-circle {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; flex-shrink: 0; font-size: .875rem;
}
.step-circle.done { background: #f97316; color: white; }
.step-circle.pending { background: #e2e8f0; color: #64748b; }
.step-label { font-size: .875rem; white-space: nowrap; }

.shipping-option {
  border: 2px solid #e2e8f0; border-radius: 12px;
  padding: 16px 20px; cursor: pointer;
  transition: all .2s;
}
.shipping-option:hover { border-color: #f97316; }
.shipping-option.selected { border-color: #f97316; background: #fff7ed; }
</style>
