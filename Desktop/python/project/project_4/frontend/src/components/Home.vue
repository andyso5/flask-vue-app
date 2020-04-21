
<template>
  <div>
    <p>Home page</p>
    <!-- <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button> -->
    <div>
      <a href="/table">查看数据库</a>
      <span>    </span>
      <a href="/edit-code">编辑代码查询</a>
      <span>    </span>
      <a href="/manager">仓库管理</a>

    </div>
  </div>
  
</template>

<script>
import axios from 'axios'
export default{
  data () {
    return {
      randomNumber: 0
    }
  },
  methods: {
    // getRandom () {
    //   // this.randomNumber = this.getRandomInt(1, 100)
    //   this.randomNumber = this.getRandomFromBackend()

    // },
    getRandom () {
      const path = 'http://localhost:5000/api/random'
      axios.get(path).then(response => {
        this.randomNumber = response.data.randomNumber
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>