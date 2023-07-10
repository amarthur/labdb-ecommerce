<template>
  <div id="app">
    <div class="navbar">
      <img src="@/assets/logo.png" alt="Logo" class="logo"/>
      <input type="text" placeholder="Search..." :class="['search', isLoggedIn ? 'search-logged-in' : 'search-logged-out']"/>
      <div class="buttons" v-if="!isLoggedIn">
        <button class="btn login" @click="showLoginModel">Log In</button>
        <button class="btn join" @click="showJoinModel">Join</button>
      </div>
      <div class="user-section" v-else>
        <button class="btn create-event" @click="showCreateEventModal">Create Event</button>
        <div class="dropdown" @click="toggleDropdown">
          <img class="user-profile" src="@/assets/owners/uspcodelab.png" alt="User Profile">
          <div class="dropdown-content" v-show="isDropdownShown">
            <button class="btn logout" @click="handleLogout">Log Out</button>
          </div>
        </div>
      </div>
      <LoginModel ref="LoginModel" @login-success="handleLoginSuccess" />
      <JoinModel ref="JoinModel" />
      <CreateEventModal ref="CreateEventModal" />
    </div>

    <h1 class="title">Event Feed</h1>
    <div class="entity-feed">
      <EntitiesList :entities="entities" v-if="entities" />
    </div>
    <div class="event-feed">
      <EventPost v-for="event in sortedEvents" :key="event.id" :event="event" />
    </div>
  </div>
</template>

<script>
import EventPost from './components/EventPost.vue';
import LoginModel from './components/LoginModel.vue';
import CreateEventModal from './components/CreateEventModal.vue';
import JoinModel from './components/JoinModel.vue';
import EntitiesList from './components/EntitiesList.vue';

export default {
  name: 'App',
  components: {
    EventPost,
    LoginModel,
    JoinModel,
    CreateEventModal,
    EntitiesList,
  },
  data() {
    return {
      events: [],
      isLoggedIn: false,
      isDropdownShown: false,
    }
  },
  created() {
    this.fetchEvents()
  },
  methods: {
    handleJoin() {
      // handle join logic here
      console.log('Join button clicked');
    },
    showLoginModel() {
      this.$refs.LoginModel.showLoginModel();
    },
    showJoinModel() {
      this.$refs.JoinModel.showJoinModal();
    },
    handleLoginSuccess() {
      this.isLoggedIn = true;
    },
    showCreateEventModal() {
      this.$refs.CreateEventModal.showCreateEventModal();
    },
    toggleDropdown() {
      this.isDropdownShown = !this.isDropdownShown;
    },
    handleLogout() {
      // logout logic
      this.isLoggedIn = false;
    },
    fetchEvents() {
      fetch('http://localhost:5000/api/events')
      .then(response => response.json())
      .then(data => {
        this.events = data.map(event => ({
          ...event,
          date: new Date(Date.parse(event.date || event.datetime)),
          imageURL: require('@/assets/events/' + event.imageURL),
          ownerImageURL: require('@/assets/owners/' + event.ownerImageURL)
        }));
      })
      .catch(error => {
        console.error('Error fetching events:', error);
      });
    }
  },
  computed: {
  sortedEvents() {
    return this.events.slice().sort((a, b) => a.date - b.date);
  }
}
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  margin: 0 auto;
}

h1 {
  text-align: center;
}

.event-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.event-card img {
  width: 80%;
  height: auto;
  object-fit: cover;
  border-radius: 15px;
  max-height: 200px;
}

.event-card .date {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.event-card .description {
  font-size: 1.1rem;
  color: #343a40;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.2em 1em;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  width: 100%;
  max-width: 97%;
  margin: auto;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-right {
  display: flex;
  gap: 1em;
  margin-right: 2em;
}
.logo {
  width: 70px;
  height: auto;
}

.search {
  margin: 0 1em;
  padding: 0.5em;
  border: none;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-logged-out {
  flex-grow: 1;
}

.search-logged-in {
  flex-grow: 0.95;
}

.buttons {
  display: flex;
  align-items: center;
  gap: 1em;
}

.btn {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

.btn.login {
  background-color: #6c757d;
}

.btn.login:hover {
  background-color: #5a6268;
}
.btn.create-event {
  background-color: #54bb00;
}
body {
  padding-top: 50px;
}

.user-profile {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-left: 10px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1em;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 120px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  padding: 12px 16px;
  z-index: 1;
  right: 0;
  top: 100%;
}

.dropdown-content button {
  background: none;
  color: black;
  padding: 0;
  margin: 0;
  border: none;
  text-decoration: none;
  width: 100%;
  text-align: left;
}

.dropdown:hover .dropdown-content {
  display: block;
}

</style>
