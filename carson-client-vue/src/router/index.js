import Vue from 'vue'
import Router from 'vue-router'
import Chatbot from '@/components/ChatBot'
import Welcome from '@/components/Welcome'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: Welcome
    },
    {
      path: '/ChatBot',
      name: 'Chatbot',
      component: Chatbot
    }
  ]
})
