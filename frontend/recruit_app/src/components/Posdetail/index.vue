<template>
  <div class="posdetail">
    <div class="pos-header">
      <div class="container">
        <el-row>
          <el-col :span="16">
            <div class="grid-content">
              <div class="mid-wrapper">
                <p class="pos-name">{{ position.positionName }}</p>
                <p class="pos-require">
                  <span class="pos-salary"><i class="el-icon-money"></i> {{ position.salary }}</span>
                  <span><i class="el-icon-location-information"></i> {{ position.city }}</span>
                  <span><i class="el-icon-time"></i> 经验{{ position.workYear }}</span>
                  <span><i class="el-icon-medal"></i> {{ position.education }}</span>
                  <span><i class="el-icon-date"></i> {{ position.jobNature }}</span>
                </p>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="grid-content">
              <div class="operate">
                <div class="btn-wrapper">
                  <a href="javascript:;" @click="deliveryResume"><i class="el-icon-position"></i> 投递</a>
                  <a href="javascript:;"><i class="el-icon-star-off"></i> 收藏</a>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    <div class="pos-content">
      <div class="container">
        <el-row>
          <el-col :span="16">
            <div class="grid-content">
              <div class="pos-intro">
                <h1 class="sub-title">职位诱惑</h1>
                <p>{{ position.positionAdvantage }}</p>
                <h1 class="sub-title">职位描述</h1>
                <p v-html="position.positionIntroHtml"></p>
                <h1 class="sub-title">工作地址</h1>
                <p>{{ position.city }}-{{ position.district }}-{{ position.subwayLine +""+ position.stationName }}</p>
                <h1 class="sub-title">发布用户</h1>
                <div class="publisher">
                  <div class="avatar"><el-avatar shape="circle" :size="60" :src="position.publisher.avatar"></el-avatar></div>
                  <div class="info">
                    <span><a :href="`/user/${position.publisher.id}`">{{ position.publisher.nic_name }}</a></span>
                    <span>{{ position.create_time | dateStr }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="grid-content">
              <div class="com-intro">
                <div class="com-avatar">
                  <img :src="`${this.settings.Host + position.company.companyLogo}`">
                </div>
                <p class="com-name">{{ position.company.companyShortName }}</p>
                <p><i class="el-icon-aim"></i> {{ position.company.industryField }}</p>
                <p><i class="el-icon-finished"></i> {{ position.company.financeStage }}</p>
                <p><i class="el-icon-user"></i> {{ position.company.companySize }}</p>
                <p><i class="el-icon-link"></i> <a :href=position.company.companySite>{{ position.company.companySite }}</a></p>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: 'posdetail',
  data () {
    return {
      pos_id: '',
      user_id: '',
      position: []
    }
  },
  filters: {
    dateStr: function(value, format="YYYY-MM-DD HH:mm:ss") {
      return moment(value).format(format);
    },
    endOf: function(value, format = "YYYYMMDD") {
      return moment(value, "YYYYMMDD").fromNow();
    }
  },
  created () {
    this.pos_id = this.$route.params.id;
    this.user_id = sessionStorage.user_id;
    this.getPosition();
  },
  methods: {
    async getPosition () {
      let response = await this.axios.get(`${this.settings.Host}/home/position/${this.pos_id}/`)
      this.position = response.data
    },
    deliveryResume () {
      this.axios.post(`${this.settings.Host}/delivery/`, {
        user: this.user_id,
        position: this.pos_id
      }).then(res => {
        this.$notify({
          title: '成功',
          message: '简历已投递，请耐心等待回复',
          type: 'success'
        });
      }).catch(err => {
        this.$notify({
          title: '失败',
          message: '简历已投递过了，不要重复投递哦',
          type: 'error'
        });
      })
    }
  }
}
</script>

<style lang="less" rel="stylesheet/less">
.posdetail {
  .pos-header {
    background-color: #f9f9f9;
    .container {
      .el-row {
        margin-bottom: 20/16rem;
        padding: 20/16rem 0;
        &:last-child {
          margin-bottom: 0;
        }
        .el-col {
          border-radius: 4/16rem;
          .grid-content {
            border-radius: 4/16rem;
            min-height: 36/16rem;
            height: 140/16rem;
            .row-bg {
              padding: 10/16rem 0;
              background-color: #f9fafc;
            }
            .mid-wrapper {
              display: flex;
              padding: 0 60/16rem;
              height: inherit;
              justify-content: flex-end;
              flex-direction: column;
              .pos-name {
                height: 30/16rem;
                margin-bottom: 10/16rem;
                line-height: 30/16rem;
                font-size: 25/16rem;
                color: #444;
                font-weight: 200;
              }
              .pos-require {
                display: flex;
                justify-content: space-between;
                height: 30/16rem;
                line-height: 30/16rem;
                span {
                  font-size: 16/16rem;
                  color: #757575;
                  i {
                    color: #757575;
                  }
                }
                .pos-salary {
                  color: #dd4a38;
                  font-size: 20/16rem;
                  font-weight: 600;
                }
              }
            }
            .operate {
              height: inherit;
              position: relative;
              .btn-wrapper {
                position: absolute;
                height: 40px;
                display: flex;
                bottom: 0;
                padding: 0 60/16rem;
                justify-content: space-between;
                flex-direction: row;
                a {
                  display: block;
                  height: 2.5rem;
                  width: 120px;
                  line-height: 2.5rem;
                  text-align: center;
                  color: #fff;
                  font-size: 1rem;
                  background-color: #333;
                  border-radius: 0.25rem;
                  -webkit-transition: all 0.3s;
                  transition: all 0.3s;
                  &:hover {
                    box-shadow: 0 0.9375rem 1.875rem rgba(0, 0, 0, 0.1);
                    transform: translate3d(0, -0.125rem, 0);
                    /*color: #333;*/
                    background-color: #000;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  .pos-content {
    .container {
      .el-row {
        margin-bottom: 20/16rem;
        &:last-child {
          margin-bottom: 0;
        }
        .el-col {
          border-radius: 4/16rem;
          .grid-content {
            border-radius: 4/16rem;
            min-height: 36/16rem;
            .pos-intro {
              padding: 20/16rem 60/16rem;
              border-right: 1/16rem dashed #ddd;
              .sub-title {
                height: 30/16rem;
                line-height: 30/16rem;
                font-size: 20/16rem;
                color: #444;
                margin-bottom: 10/16rem;
              }
              p {
                margin-bottom: 0.625rem;
                font-size: 1rem;
                color: #444;
                padding: 10px;
                line-height: 1.875rem;
                background-color: #f9f9f9;
                border-radius: 5px;
              }
              .publisher {
                display: flex;
                div {
                  height: 60px;
                  margin-right: 10px;
                }
                .info {
                  flex-grow: 1;
                  span {
                    display: flex;
                    flex-direction: column;
                    line-height: 30px;
                    color: #333;
                    a {
                      color: #333;
                    }
                  }
                }
              }
            }
            .com-intro {
              padding: 20/16rem 60/16rem;
              .com-avatar {
                text-align: center;
                margin-bottom: 10/16rem;
                img {
                  width: 100/16rem;
                  height: inherit;
                  padding: 4/16rem;
                  background-color: #afafaf;
                  vertical-align: middle;
                }
              }
              p {
                height: 30/16rem;
                line-height: 30/16rem;
                margin-bottom: 10/16rem;
                color: #757575;
                a {
                  color: #757575;
                  &:hover {
                    color: #2b84f1;
                  }
                }
              }
              .com-name {
                text-align: center;
                font-size: 20/16rem;
                font-weight: 200;
                color: #333;
              }
            }
          }
        }
        .row-bg {
          padding: 10/16rem 0;
          background-color: #f9fafc;
        }
      }
    }
  }
}
</style>
