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
      <img class="inputElement inputButton" @click="recording ? stopRecording : startRecording" src="../assets/speak.png"/>
      <div class="inputElement" id="inputWrap"><input id="theInput" @keyup.enter="sendMessage" placeholder="Ask me anything"/></div>
      <img class="inputElement inputButton" id="send" src="../assets/send.svg" @click="sendMessage"/>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
const $ = require('jQuery')
const Recorder = require('../../dist/recorder.js')
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      loading: false,
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
      ],
      recorder: null,
      audio_context: null,
      recording: false
    }
  },
  mounted: function () {
    const vm = this
    vm.scrollToBottom('#messageZone')
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;
      vm.audio_context = new AudioContext;
    } catch (e) {
      alert('No web audio support in this browser!');
    }
    navigator.getUserMedia({audio: true}, vm.startUserMedia, function(e) {
      console.log("fail")
    });
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
        vm.loading = true
        $.get(encodeURI('http://b99052d7.ngrok.io/api/converse?text=' + data), function (result) {
          let resp = JSON.parse(result)
          vm.loading = false
          vm.messages.push({from: 0, content: resp.response || 'ERROR'})
        })
      }
    },
    scrollToBottom: function (id) {
      var div = $(id)
      var height = div[0].scrollHeight
      div.scrollTop(height)
    },
    createAudioElement: function (blobUrl) {
        const downloadEl = document.createElement('a');
        downloadEl.style = 'display: block';
        downloadEl.innerHTML = 'download';
        downloadEl.download = 'audio.webm';
        downloadEl.href = blobUrl;
        const audioEl = document.createElement('audio');
        audioEl.controls = true;
        const sourceEl = document.createElement('source');
        sourceEl.src = blobUrl;
        sourceEl.type = 'audio/webm';
        audioEl.appendChild(sourceEl);
        document.body.appendChild(audioEl);
        document.body.appendChild(downloadEl);
    },
    startUserMedia: function (stream) {
      const vm = this;
      console.log("starting Media")
      var input = vm.audio_context.createMediaStreamSource(stream);
      // Uncomment if you want the audio to feedback directly
      //input.connect(audio_context.destination);
      //__log('Input connected to audio context destination.');
      vm.recorder = new Recorder(input);
    },
    startRecording: function (button) {
      const vm = this;
      console.log("start record")
      vm.recording = true
      vm.recorder && vm.recorder.record();
    },
    stopRecording: function (button) {
      const vm = this;
      console.log("stoping")
      vm.recorder && vm.recorder.stop();
      vm.recording = false;
      button.disabled = true;
      
      // create WAV download link using audio data blob
      vm.createDownloadLink();
      vm.recorder.clear();
    },
    createDownloadLink: function () {
      vm.recorder && vm.recorder.exportWAV(function(blob) {
      var url = URL.createObjectURL(blob);
      var li = document.createElement('li');
      var au = document.createElement('audio');
      var hf = document.createElement('a');
      
      au.controls = true;
      au.src = url;
      hf.href = url;
      hf.download = new Date().toISOString() + '.wav';
      hf.innerHTML = hf.download;
      li.appendChild(au);
      li.appendChild(hf);
      recordingslist.appendChild(li);
    })
  }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="SASS">
$black : #151515;
$gold : rgb(195, 156, 104);
@font-face {
  font-family: "Museo";
  src: url('../assets/Museo.otf') format('truetype')
}
textarea:focus, input:focus{
  outline: none;
}
input {
  border: none;
}
.body {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 0px;
  font-family: 'Museo';
  #messageZone {
    margin-top: 115px;
    height: calc(100% - 202px);
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
