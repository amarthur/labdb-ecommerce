<template>
  <div class="event-post">
    <div class="owner-info">
      <img :src="`${event.ownerImageURL}`" alt="Owner image" class="owner-img" />
      <p>{{ event.owner }}</p>
    </div>
    <h2>{{ event.title }}</h2>
    <p>Date:  {{ event.date.toLocaleDateString() }}</p>
    <p>{{ event.description }}</p>
  </div>
</template>

<script>
export default {
  name: 'EventPost',
  props: {
    event: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.event-post {
  width: 80%;
  max-width: 600px;
  max-height: 800px;
  border-radius: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
  margin: 1rem auto;
  padding: 1rem;
  overflow: hidden;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;

}

.owner-info {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

.owner-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}


.event-post h2 {
  font-size: 1.2rem;
  color: #343a40;
  margin-bottom: 0.5rem;
}

.event-post p {
  font-size: 1rem;
  color: #6c757d;
}
</style>