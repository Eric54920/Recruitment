<template>
  <div class="followed-item">
      <div class="avatar">
            <img class="img" :src="item.avatar" />
      </div>
      <div class="nic_name">
            <el-link :underline="false" :href="`/user/${item.pk}`">{{ item.nic_name }}</el-link>
      </div>
      <div class="operate">
          <span>发送消息</span>
          <span @click="focus(item.pk)" v-html="focus_btn"></span>
      </div>
  </div>
</template>

<script>
export default {
    data () {
        return {
            user_id: "",
            focus_btn: "<i class='fa fa-user-plus'> 取消关注</i>",
        }
    },
    created () {
        this.user_id = sessionStorage.user_id
    },
    props: {
        item: {
            type: Object,
            require: true
        }
    },
    methods: {
        // 关注
        focus (uid) {
            if (this.user_id == uid) {
                this.$message('自己不能关注自己');
            } else if (!this.user_id) {
                this.$message('请先登录');
            } else {
                this.axios.post(`${this.settings.Host}/user/focus/`, {
                "follower": this.user_id,
                "followed": uid
                }).then(res => {
                    if (res.data.action == 'cancel') {
                        this.focus_btn = "<i class='fa fa-user-plus'> 关注</i>";
                        // this.getFocusInfo();
                    } else if(res.data.action == 'focus') {
                        this.focus_btn = "<i class='fa fa-user-plus'> 取消关注</i>";
                        // this.getFocusInfo();;
                    }
                }).catch(err => {
                    this.$message('网络异常');
                })
            }
        }
    }
}
</script>

<style lang="less" rel="stylesheet/less">
.followed-item {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    line-height: 50px;
    background: #fff;
    border-radius: 10px;
    margin-bottom: 20px;
    .avatar {
        display: inline-block;
        height: 50px;
        width: 50px;
        border-radius: 50%;
        vertical-align: middle;
        overflow: hidden;
        box-shadow: 0 0 0 2px #fff, 0 0 0 3px #128ffd,
            0 8px 16px 0 rgba(0, 0, 0, 0.15);
        .img {
            height: inherit;
            width: inherit;
        }
    }
    .nic_name {
        flex-grow: 1;
        padding-left: 20px;
    }
    .operate {
        display: flex;
        width: 180px;
        justify-content: space-between;
        align-items: center;
        span {
            display: inline-block;
            height: 35px;
            padding: 0 10px;
            margin: 5px 0;
            float: right;
            box-sizing: border-box;
            border: 2px solid #eee;
            line-height: 31px;
            border-radius: 22px;
            font-size: 14px;
            color: #666;
            transition: all .3s;
            cursor: pointer;
            &:hover {
              color: #333;
              border: 2px solid #999;
            }
          }
    }
}
</style>