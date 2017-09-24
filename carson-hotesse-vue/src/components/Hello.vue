<template>
  <div>
    <div id="body">
      <img :src="imagePath(tab)"/>
    </div>
    <div id="nav">
      <div :class="'navWrap' + (tab == 1 ? ' active' : '')">
        <img src="../assets/icon1.png" @click="changeTab(1)"/>
      </div>
      <div :class="'navWrap' + (tab == 2 ? ' active' : '')">
        <img src="../assets/icon2.png" @click="changeTab(2)"/>
      </div>
      <div :class="'navWrap' + (tab == 3 ? ' active' : '')">
        <img src="../assets/icon3.png" @click="changeTab(3)"/>
      </div>
      <div :class="'navWrap' + (tab == 4 ? ' active' : '')">
        <img src="../assets/icon4.png" @click="changeTab(4)"/>
      </div>
      <div :class="'navWrap' + (tab == 5 ? ' active' : '')">
        <img src="../assets/icon5.png" @click="changeTab(5)"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      tab: 1
    }
  },
  methods: {
    changeTab: function (nb) {
      const vm = this
      vm.tab = nb
    },
    imagePath: function (nb) {
      return require('../assets/page' + this.tab + '.png')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="SASS">

$gold : rgb(195, 156, 104);

@font-face {
  font-family: "Museo";
  src: url('../assets/Museo.otf') format('truetype')
}

#nav {
  position: sticky;
  bottom: 0px;
  width: 100%;
  background-color: white;
  .navWrap {
    display: inline-block;
    padding: 20px 40px;
    img {
      width: 100px;
    }
  }
  .active {
    background-color: $gold;
  }
}
#body {
  width: 100%;
  height: 100%;
  img {
    width: 100%;
  }
}
</style>
