<template>
  <div class="body">
    <div id="messageZone">
      <div id="messagesWapper">
        <div v-for="message in messages" class="messageContainer">
          <span :class="message.from ? 'right' : 'left'">{{message.content}}</span>
        </div>
        <div v-if="loading" class="messageContainer">
          <loading class="left"></loading>
        </div>
      </div>
    </div>
    <div id="inputZone">
      <img class="inputElement inputButton" src="../assets/speak.png"/>
      <div class="inputElement" id="inputWrap"><input id="theInput" @keyup.enter="sendMessage" placeholder="Ask me anything"/></div>
      <img class="inputElement inputButton" id="send" src="../assets/send.svg" @click="sendMessage"/>
    </div>
  </div>
</template>

<script>
const $ = require('jQuery')
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      loading: true,
      messages: [
        {
          from: 0, // CARSON
          content: 'Bonjour.'
        },
        {
          from: 1, // CLIENT
          content: 'je veux du pain.'
        },
        {
          from: 0, // CARSON
          content: 'Ce sera fait. Autre chose ?'
        },
        {
          from: 1, // CLIENT
          content: 'Non.'
        },
        {
          from: 0, // CARSON
          content: 'Tres bien.'
        }
      ]
    }
  },
  updated: function () {
    const vm = this
    vm.scrollToBottom('#messageZone')
  },
  methods: {
    sendMessage: function (event) {
      const vm = this
      const data = $('#theInput').val()
      if (data) {
        $('#theInput').val('')
        vm.messages.push({from: 1, content: data})
      }
    },
    scrollToBottom: function (id) {
      var div = $(id)
      var height = div[0].scrollHeight
      div.scrollTop(height)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="SASS">
$black : #151515;
$gold : rgb(195, 156, 104);
textarea:focus, input:focus{
    outline: none;
}
.body {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  #messageZone {
    margin-top: 150px;
    height: 440px;
    overflow-y: scroll;
    .messagesWrapper {
    }
    .messageContainer {
      display: block;
      width: 100%;
      overflow: hidden;
      margin-top: 20px;
      .left {
        float: left;
        padding: 10px;
        border-radius: 10px;
        background-color: $black;
        color: white;
      }
      .right {
        float: right;
        padding: 10px;
        border-radius: 10px;
        background-color: $gold;
        color: white;
      }
    }
  }
  #inputZone {
    bottom: 0px;
    position: absolute;
    width: 100%;
    padding-top: 3px;
    border-top: 2px solid #151515;
    .inputElement {
      display: inline-block;
      vertical-align: top;
    }
    #inputWrap {
      width: calc(100% - 85px);
      margin-left: 5px;
      input {
        width: 100%;
        line-height: 100%;
        height: 40px;
        font-size: 20px;
      }
    }
    .inputButton {
      width: 30px;
    }
    .inputButton:hover {
      cursor: pointer;
    }
    #send {
      margin-left: 10px;
      margin-top: 7px;
    }
  }
}
</style>
