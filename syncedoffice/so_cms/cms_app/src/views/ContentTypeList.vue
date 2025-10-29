<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Content Types</h1>
        <p class="mt-1 text-sm text-gray-500">
          Create and manage your content structure
        </p>
      </div>
      <BaseButton @click="createNew">
        <Plus :size="16" class="mr-2" />
        Create Content Type
      </BaseButton>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !contentTypes.length" class="text-center py-12">
      <div class="inline-block animate-spin text-4xl">⟳</div>
      <p class="mt-2 text-gray-500">Loading content types...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && !contentTypes.length" class="text-center py-12">
      <FileText :size="48" class="mx-auto text-gray-400 mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">No content types yet</h3>
      <p class="text-gray-500 mb-6">Get started by creating your first content type</p>
      <BaseButton @click="createNew">
        Create Content Type
      </BaseButton>
    </div>

    <!-- Content Types Grid -->
    <div v-else>
      <!-- Collection Types -->
      <div v-if="collectionTypes.length" class="mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Collection Types</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ContentTypeCard
            v-for="ct in collectionTypes"
            :key="ct.name"
            :content-type="ct"
            @edit="editContentType"
            @delete="confirmDelete"
          />
        </div>
      </div>

      <!-- Single Types -->
      <div v-if="singleTypes.length">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Single Types</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ContentTypeCard
            v-for="ct in singleTypes"
            :key="ct.name"
            :content-type="ct"
            @edit="editContentType"
            @delete="confirmDelete"
          />
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <ConfirmDialog
      v-if="showDeleteDialog"
      title="Delete Content Type"
      :message="`Are you sure you want to delete '${contentTypeToDelete?.display_name}'? This action cannot be undone.`"
      confirm-text="Delete"
      confirm-variant="danger"
      @confirm="handleDelete"
      @cancel="showDeleteDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useContentTypeStore } from '../stores/contentTypeStore'
import { Plus, FileText } from 'lucide-vue-next'
import BaseButton from '../components/BaseButton.vue'
import ContentTypeCard from '../components/ContentTypeCard.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const router = useRouter()
const store = useContentTypeStore()

const showDeleteDialog = ref(false)
const contentTypeToDelete = ref(null)

const contentTypes = computed(() => store.contentTypes)
const collectionTypes = computed(() => store.collectionTypes)
const singleTypes = computed(() => store.singleTypes)
const loading = computed(() => store.loading)

onMounted(() => {
  store.fetchContentTypes()
})

function createNew() {
  router.push('/cms/content-types/new')
}

function editContentType(contentType) {
  router.push(`/cms/content-types/${contentType.name}`)
}

function confirmDelete(contentType) {
  contentTypeToDelete.value = contentType
  showDeleteDialog.value = true
}

async function handleDelete() {
  try {
    await store.deleteContentType(contentTypeToDelete.value.name)
    showDeleteDialog.value = false
    contentTypeToDelete.value = null
  } catch (error) {
    alert('Error deleting content type: ' + error.message)
  }
}
</script>
