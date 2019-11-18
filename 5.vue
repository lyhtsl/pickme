<template>
  <view id="comunication">
    <span class="resData">get请求到的数据：{{resData}}</span>
	<br /> <br />
    <span class="postData">post请求到的数据：{{postData}}</span>
  </view>
</template>
<script>
  export default {
    data (){
      return {
          resData:[],
        postData:[]
      }
    },
	onLoad() {
		this.doGet(),
		this.doPost()
	},
    methods: {
      doGet(){
        // 发起get请求
    uni.request({
    url: 'http://127.0.0.1/driver/quikcar/tkod', //仅为示例，并非真实接口地址。
    data: {
        oid:'4',
		did:'2'
    },
    success: (res) => {
        console.log(res.data);
        this.resData =res.data;
    }
});
      },
      doPost(){
		uni.request({
		url: 'http://127.0.0.1/login', //仅为示例，并非真实接口地址。
		data: {
		   user:'123',
		   pwd:'23'
		},

		method:"POST",
		success: (res) => {
		    console.log(res.data);
		    this.postData =res.data ;
		}
      });
    }
  },
  }
</script>

</style>