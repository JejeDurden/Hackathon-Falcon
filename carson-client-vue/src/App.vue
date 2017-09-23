<template>
  <div id="app">
    <img src="./assets/carsonLogo.png"/>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style scoped lang="SASS">
body, html {
  margin: 0px;
  height: 100%;
  width: 100%;
  overflow: hidden;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 30px;
  text-align: center;
  img {
    z-index: 1000;
    width: 150px;
  }
}

</style>
