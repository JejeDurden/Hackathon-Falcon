<template>
  <div>
    <div class="background">
      <img src="../assets/background.png"/>
    </div>
    <div class="body">
      <div class="actionButtonWrap">
        <div class="buttonPastron"></div>
        <div class="buttonPastron"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="SASS">
.background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  img {
    width: 100%;
    height: 100%;
  }
}
.body {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  .actionButtonWrap {
    top: 100px;
    position: absolute;
    transform: translateX(-50%);
    left: 50%;
    .buttonPastron {
      background-color: #000;
      border-radius: 50%;
      height: 35px;
      width: 35px;
      margin-top: 85px;
    }
  }
}

</style>
