<template>
    <div class="view-all">
      <h1 class="title">{{ entityName }}</h1>
      <div class="items-container">
        <div v-for="(item, index) in items" :key="index" class="item">
          <div v-for="(value, key) in item" :key="key" class="item-field">
            <p class="field-key"><strong>{{ key }}: </strong></p>
            <p class="field-value">{{ Array.isArray(value) ? value.join(', ') : value }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        entityName: '',
        items: []
      }
    },
    async mounted() {
        try {
            const entityName = this.$route.params.entityName;
            this.entityName = entityName.charAt(0).toUpperCase() + entityName.slice(1); // to capitalize the first letter for display
            const data = await import(`@/assets/mocks/sql/${entityName.toLowerCase()}.json`); // Import the correct file based on the lowercased entityName
            this.items = data.default[entityName.toLowerCase()]; // Use the lowercase entityName
        } catch (e) {
            console.log('There was a problem with the import operation: ' + e.message);
        }
    }

}
</script>


<style scoped>
.view-all {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
}

.title {
  color: #333;
  margin-bottom: 2rem;
}

.items-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem; /* Adds space between the items */
}

.item {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 10px; /* Gives rounded corners */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Adds a subtle shadow */
  width: 300px;
}

.item-field {
  margin-bottom: 0.5rem;
}

.field-key {
  font-weight: bold;
}

.field-value {
  color: #666;
}
</style>