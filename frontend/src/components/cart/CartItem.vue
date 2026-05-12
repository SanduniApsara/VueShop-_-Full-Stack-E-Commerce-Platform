<template>
  <div class="d-flex gap-3 py-3 border-bottom">
    <img
      :src="item.product.image || '/placeholder.jpg'"
      :alt="item.product.name"
      class="rounded-2 object-fit-cover flex-shrink-0"
      style="width: 72px; height: 72px;"
    />
    <div class="flex-grow-1 min-w-0">
      <p class="fw-medium text-sm mb-1 text-truncate">{{ item.product.name }}</p>
      <p class="text-orange-500 fw-bold mb-2">${{ item.product.price }}</p>

      <div class="d-flex align-items-center justify-content-between">
        <!-- Qty controls -->
        <div class="d-flex align-items-center border rounded-pill overflow-hidden">
          <button @click="decrement" class="btn btn-sm px-2 py-0 border-0">−</button>
          <span class="px-2 small fw-medium">{{ item.quantity }}</span>
          <button @click="increment" class="btn btn-sm px-2 py-0 border-0">+</button>
        </div>

        <!-- Line total -->
        <span class="fw-semibold text-sm">${{ Number(item.line_total).toFixed(2) }}</span>

        <!-- Remove -->
        <button @click="$emit('remove')" class="btn btn-link text-danger p-0 text-decoration-none small">
          🗑
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  item: { type: Object, required: true }
})
const emit = defineEmits(['remove', 'update'])

function increment() { emit('update', props.item.quantity + 1) }
function decrement() {
  if (props.item.quantity > 1) emit('update', props.item.quantity - 1)
  else emit('remove')
}
</script>
