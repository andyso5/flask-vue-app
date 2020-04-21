import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

// Vue.use(Router)

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       component: 'Home'
//     },
//     {
//       path: '/about',
//       components: 'About'
//     }
//   ]
// })

const routerOptions = [
  { path: '/', component: 'Home' },//'Home'默认指向'../components/Home.vue'
  { path: '/about', component: 'About' },
  { path: '*',component: "NotFound" },//通配符 '*' 在 vue-router 里的含义是以上路由定义之外的情况
  { path: '/edit-code', component: 'CODE'},
  { path: '/table', component: 'TABLE'},
  { path: '/graph', component:'GRAPH'},
  { path: '/manager', component:'MANAGER'},
  { path: '/richtext', component:'RICHTEXT'},
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})