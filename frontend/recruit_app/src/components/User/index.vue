<template>
  <div class="manage">
    <div class="top-banner" v-bind:style="{ backgroundImage: 'url('+ bannerImg +')'}"></div>
    <div class="info-first">
      <div class="container">
        <div class="left">
          <span class="img-wrapper" v-bind:style="{ backgroundImage: 'url('+userInfo.avatar +')'}"></span>
        </div>
        <div class="right">
          <div class="name">
            <p><span class="nic_name">{{ userInfo.nic_name }}</span> <span class="focus" v-html="focus_btn" @click="focus"></span></p>
            <span class="edit-profile" @click="dialogFormVisible = true">
              <i class="el-icon-view"></i> 查看资料
            </span>
          </div>
          <p class="intro">{{ userInfo.intro }}</p>
          <p class="social">
            <a v-if="userInfo.site" :href="userInfo.site" target="_blank">
              <i class="fa fa-home"></i>
            </a>
            <a v-if="userInfo.facebook" :href="userInfo.facebook" target="_blank">
              <i class="fa fa-facebook"></i>
            </a>
            <a v-if="userInfo.twitter" :href="userInfo.twitter" target="_blank">
              <i class="fa fa-twitter"></i>
            </a>
            <a v-if="userInfo.weibo" :href="userInfo.weibo" target="_blank">
              <i class="fa fa-weibo"></i>
            </a>
            <a v-if="userInfo.email" :href="'mailto:'+userInfo.email" target="_blank">
              <i class="fa fa-envelope-o"></i>
            </a>
            <a v-if="userInfo.github" :href="userInfo.github" target="_blank">
              <i class="fa fa-github"></i>
            </a>
          </p>
        </div>
      </div>
    </div>
    <div class="info-second">
      <div class="container">
        <el-row :gutter="20">
          <el-col :span="5">
            <div class="grid-content">
              <div class="info-saide">
                <p class="follow">
                  <span>
                    <b>{{ focus_info.follower }}</b>
                    <i>已关注</i>
                  </span>
                  <span>
                    <b>{{ focus_info.followed }}</b>
                    <i>粉丝</i>
                  </span>
                </p>
                <ul>
                  <li>
                    <a
                      :class="{'active': panel_id=='news'}"
                      href="javascript:;"
                      @click="panel_id='news';filters.page=1"
                    >
                      <i class="el-icon-files"></i> 动态
                    </a>
                  </li>
                  <li>
                    <a
                      :class="{'active': panel_id=='article'}"
                      href="javascript:;"
                      @click="panel_id='article';filters.page=1"
                    >
                      <i class="el-icon-document"></i> 文章
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </el-col>
          <el-col :span="14">
            <div class="grid-content">
              <div class="info-content" v-if="panel_id == 'news'">
                <News
                  @removeItem="refresh_list()"
                  v-for="(item, i) in news_list.results"
                  :key="i"
                  v-bind:item="item"
                  v-bind:userInfo="userInfo"
                ></News>
                <el-pagination
                  background
                  @current-change="handleCurrentChange"
                  layout="prev, pager, next"
                  :total="news_list.count"
                ></el-pagination>
              </div>
              <div class="info-content" v-if="panel_id == 'article'">
                <Articles
                  @removeItem="refresh_list()"
                  v-for="(item, i) in article_list.results"
                  :key="i"
                  v-bind:item="item"
                  v-bind:userInfo="userInfo"
                ></Articles>
                <el-pagination
                  background
                  @current-change="handleCurrentChange"
                  layout="prev, pager, next"
                  :total="article_list.count"
                ></el-pagination>
              </div>
            </div>
          </el-col>
          <el-col :span="5">
            <div class="grid-content">
              <!-- <div class="comment-saide" >
                <p class="comment-title">最近评论</p>
                <ul class="comment-wrapper">
                  <li class="comment-item">
                    <div class="pub-time">
                      <span>2020</span>
                      <span class="month">Mar</span>
                      <span>23</span>
                    </div>
                    <p class="comment">阿达胡说八道讲哈不是大家哈是的哈是多久啊</p>
                  </li>
                  <li class="comment-item">
                    <div class="pub-time">
                      <span>2020</span>
                      <span class="month">Mar</span>
                      <span>23</span>
                    </div>
                    <p class="comment">阿达胡说八道讲哈不是大家哈是的哈是多久啊</p>
                  </li>
                  <li class="comment-item">
                    <div class="pub-time">
                      <span>2020</span>
                      <span class="month">Mar</span>
                      <span>23</span>
                    </div>
                    <p class="comment">阿达胡说八道讲哈不是大家哈是的哈是多久啊</p>
                  </li>
                </ul>
              </div> -->
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    <el-dialog title="资料" :visible.sync="dialogFormVisible">
      <el-tabs v-model="activeName">
        <el-tab-pane label="基本信息" name="first">
            <div class="base">
                <div class="avatar">
                    <el-avatar :size="120" v-if="userInfo.avatar" :src="userInfo.avatar" fit="cover"></el-avatar>
                </div>
                <div class="info">
                    <p><span>昵称：{{ userInfo.nic_name }}</span><span>性别：<i class="el-icon-male" v-if="userInfo.gender==1"></i><i v-else class="el-icon-female"></i></span><span>生日：{{ userInfo.birthday }}</span></p>
                    <p><span>角色：{{ userInfo.get_user_type_display }}</span><span>地区：{{ userInfo.city }}</span><span>公司：{{ userInfo.company.companyName }}</span></p>
                    <p><span>状态：{{ userInfo.work_status | status }}</span><span>职位：{{ userInfo.selfPosition }}</span></p>
                </div>
            </div>
            <p class="intro">{{ userInfo.intro }}</p>
        </el-tab-pane>
        <el-tab-pane label="社交信息" name="second">
            <div class="social">
                <p class="item">
                    <span><i class="fa fa-phone"></i> {{ userInfo.mobile }}</span>
                    <span><i class="fa fa-envelope"></i> {{ userInfo.email }}</span>
                </p>
                <p class="item">
                    <span><i class="fa fa-sitemap"></i> {{ userInfo.site }}</span>
                    <span><i class="fa fa-weibo"></i> {{ userInfo.weibo }}</span>
                </p>
                <p class="item">
                    <span><i class="fa fa-github"></i> {{ userInfo.github }}</span>
                    <span><i class="fa fa-facebook"></i> {{ userInfo.facebook }}</span>
                </p>
                <p class="item">
                    <span><i class="fa fa-twitter"></i> {{ userInfo.twitter }}</span>
                </p>
            </div>
        </el-tab-pane>
        <el-tab-pane label="教育信息" name="third">
            <div class="education">
                <p class="item">
                    <span>{{ userInfo.graduatedSchool }}</span>
                    <span>{{ userInfo.unifiedAdmission | unifiedAdmission }}</span>
                    <span>{{ userInfo.education | education }}</span>
                </p>
                <p class="item">
                    <span>{{ userInfo.specialty }}专业</span>
                    <span>{{ userInfo.admissionTime }}入学</span>
                    <span>{{ userInfo.graduationTime }}毕业</span>
                </p>
            </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script>
import News from "../Profile/News/index";
import Collections from "../Profile/Collections/index";
import Articles from "../Profile/Articles/index";
import Resume from "../Profile/Resume/index";

export default {
  data() {
    return {
      activeName: "first",
      uid: '',
      user_id: "",
      bannerImg: "../../../static/imgs/banner.jpg",
      imageUrl: "",
      token: {},
      options: [
        { value: 0, label: "小学" },
        { value: 1, label: "初中" },
        { value: 2, label: "高中" },
        { value: 3, label: "专科" },
        { value: 4, label: "本科" },
        { value: 5, label: "硕士" },
        { value: 6, label: "博士" }
      ],
      userInfo: {},
      panel_id: "news", // 当前所在子页面
      news_list: [],
      article_list: [],
      dialogFormVisible: false, // 个人资料表单模态框
      formLabelWidth: "120px", // 表单label的宽度
      newsValue: "", // 动态的值
      toolbars: this.settings.toolbars, // 编辑器工具栏配置
      filters: {
        // 分页条件
        page: 1
      },
      focus_info: {},
      focus_btn: '',
    };
  },
  created() {
    this.uid = this.$route.params.id;
    this.user_id = sessionStorage.user_id;
    this.get_profile();
    this.getFocusInfo();
    this.getData();
  },
  watch: {
    panel_id() {
      this.getData();
    },
    "filters.page"() {
      this.getData();
    }
  },
  filters: {
        status: function (str) {
            switch (str) {
                case '0':
                    return "已离职";
                case '1':
                    return "在职";
                case '2':
                    return "保密";
                case '3':
                    return "已退休";
            }
        },
        endOf: function(value, format = "YYYYMMDD") {
            return moment(value, "YYYYMMDD").fromNow();
        },
        unifiedAdmission: function(str) {
            switch (str) {
                case "0":
                    return "非统招"
                case "1":
                    return "统招"
            }
        },
        education (str) {
            switch (str) {
                case 0:
                    return "小学"
                case 1:
                    return "初中"
                case 2:
                    return "高中"
                case 3:
                    return "专科"
                case 4:
                    return "本科"
                case 5:
                    return "硕士"
                case 6:
                    return "博士"
            }
        }
  },
  methods: {
    // 获取个人信息
    async get_profile() {
      const response = await this.axios.get(
        `${this.settings.Host}/profile/${this.uid}/`
      );
      this.userInfo = response.data;
    },
    async getFocusInfo() {
      const response = await this.axios.get(`${this.settings.Host}/user/focus/`, {
        params: {
          "uid": this.uid,
          "user_id": this.user_id
        }
      });
      this.focus_info = response.data;
      this.focus_btn = this.focus_info.is_focus ? '<i class="fa fa-user-plus"> 取消关注</i>' : '<i class="fa fa-user-plus"> 关注</i>';
    },
    // 获取动态，文章，收藏，简历
    async getData() {
      const response = await this.axios.get(
        `${this.settings.Host}/${this.panel_id}/?user=${this.uid}`,
        {
          params: this.filters
        }
      );
      if (this.panel_id == "news") {
        this.news_list = response.data;
      } else if (this.panel_id == "article") {
        this.article_list = response.data;
      }
    },
    // 刷新当前列表
    refresh_list() {
      this.getData();
    },
    // 处理分页
    handleCurrentChange(page) {
      this.filters.page = page;
    },
    // 关注
    focus () {
      if (this.user_id == this.uid) {
        this.$message('自己不能关注自己');
      } else if (!this.user_id) {
        this.$message('请先登录');
      } else {
        this.axios.post(`${this.settings.Host}/user/focus/`, {
          "follower": this.user_id,
          "followed": this.uid
        }).then(res => {
          if (res.data.action == 'cancel') {
            this.focus_btn = '<i class="fa fa-user-plus"> 关注</i>';
            this.getFocusInfo();
          } else if(res.data.action == 'focus') {
            this.focus_btn = '<i class="fa fa-user-plus"> 取消关注</i>';
            this.getFocusInfo();;
          }
        }).catch(err => {
          this.$message('网络异常');
        })
      }
    }
  },
  components: {
    News,
    Articles,
  }
};
</script>

<style lang="less" rel="stylesheet/less">
.manage {
  .top-banner {
    height: 200/16rem;
    background-size: cover;
  }
  .info-first {
    position: relative;
    height: 120/16rem;
    .container {
      .left {
        position: absolute;
        width: 200/16rem;
        height: 200/16rem;
        margin-right: 30/16rem;
        top: -100/16rem;
        float: left;
        .img-wrapper {
          display: inline-block;
          width: inherit;
          height: inherit;
          background-size: cover;
          border: 5/16rem solid #fff;
          box-sizing: border-box;
          border-radius: 50%;
          box-shadow: 0 0 20/16rem 0 #929292;
        }
      }
      .right {
        display: flex;
        padding-left: 20px;
        justify-content: center;
        flex-direction: column;
        height: 120/16rem;
        margin-left: 230px;
        .name {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 30px;
            font-weight: 500;
            color: #333;
            .nic_name {
                margin-right: 20px;
            }
          .focus, .edit-profile {
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
            transition: all 0.3s;
            cursor: pointer;
            &:hover {
              color: #333;
              border: 2px solid #999;
            }
          }
        }
        .intro {
          margin-bottom: 5px;
          font-size: 16px;
          color: #333;
        }
        .social {
          color: #717171;
          font-size: 14px;
          a {
            display: inline-block;
            width: 30px;
            margin-right: 10px;
            padding: 2px 5px;
            border-radius: 5px;
            text-align: center;
            color: #666;
            cursor: pointer;
            &:hover {
              color: #333;
              background-color: #eee;
            }
          }
        }
      }
    }
  }
  .info-second {
    background: #f6f6f6;
    .container {
      .el-row {
        margin-bottom: 20px;
        &:last-child {
          margin-bottom: 0;
        }
        .el-col {
          border-radius: 4px;
          .grid-content {
            border-radius: 4px;
            min-height: 36px;
            .info-saide {
              padding: 20/16rem 0;
              p {
                margin-bottom: 20/16rem;
                color: #333;
              }
              .follow {
                display: flex;
                padding: 10px 0;
                justify-content: space-around;
                flex-wrap: nowrap;
                border-radius: 10px;
                background-color: #fff;
                span {
                  display: block;
                  i {
                    display: block;
                    text-align: center;
                    color: #555;
                  }
                  b {
                    display: block;
                    text-align: center;
                    font-size: 30px;
                    font-weight: 500;
                    font-family: din-bold;
                  }
                }
              }
              ul {
                padding: 10px 20px;
                background-color: #fff;
                border-radius: 10px;
                li {
                  height: 40px;
                  line-height: 40px;
                  text-align: center;
                  a {
                    color: #333;
                    i {
                      margin-right: 20px;
                    }
                  }
                  .active {
                    color: #0094ff;
                  }
                }
              }
            }
            .info-content {
              margin: 20px 0;
              .create {
                display: block;
                padding: 20px 0;
                margin-bottom: 20px;
                padding-left: 20px;
                font-size: 32px;
                color: #333;
                background-color: #fff;
                border-radius: 10px;
              }
              .editor {
                background-color: #fff;
                border-radius: 10px;
                margin-bottom: 20px;
                #main {
                  .article-desc {
                    padding: 25px 25px 0 25px;
                  }
                  .operate {
                    padding: 10px;
                    display: flex;
                    flex-wrap: nowrap;
                    flex-direction: row-reverse;
                    a {
                      display: inline-block;
                      color: #ffffff;
                      padding: 5px 10px;
                      background-color: #2fa4fe;
                      border-radius: 5px;
                    }
                  }
                }
              }
              .resume-wrapper {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
              }
              .el-pagination {
                padding: 20/16rem;
                margin-bottom: 20/16rem;
                text-align: center;
              }
            }
            .comment-saide {
              padding: 1.25rem 0;
              .comment-title {
                font-size: 16px;
                font-weight: 500;
                color: #212121;
                margin-bottom: 15px;
              }
              .comment-wrapper {
                .comment-item {
                  display: flex;
                  justify-content: space-around;
                  flex-wrap: nowrap;
                  margin-bottom: 10px;
                  padding-bottom: 10px;
                  .pub-time {
                    width: 40/16rem;
                    display: flex;
                    justify-content: center;
                    flex-direction: column;
                    background-color: #349dff47;
                    border-radius: 3px;
                    span {
                      display: inline-block;
                      width: 40/16rem;
                      font-size: 12px;
                      text-align: center;
                      color: #004c9a;
                    }
                    .month {
                      background-color: #91c3f7;
                    }
                  }
                  .comment {
                    padding: 0 5px;
                    font-size: 14px;
                    color: #333;
                    line-height: 24px;
                    font-weight: 500;
                    background-color: #f6f6f6;
                  }
                }
                & > :not(:last-child) {
                  border-bottom: 1px dashed #7ebcfc;
                }
              }
            }
          }
        }
      }
    }
  }
  .el-dialog__wrapper {
    .el-dialog {
      .el-dialog__body {
        .el-tabs__content {
          .el-tab-pane {
            .base {
                display: flex;
                margin-bottom: 30px;
                .avatar {
                    margin-right: 30px;
                }
                .info {
                    flex-grow: 1;
                    display: flex;
                    justify-content: space-between;
                    flex-direction: column;
                    p {
                        display: flex;
                        font-size: 15px;
                        line-height: 38px;
                        span {
                            width: 33.3%;
                            text-overflow: ellipsis;
                            overflow: hidden;
                            white-space: nowrap;
                        }
                    }
                }
            }
            .intro {
                font-size: 16px;
                line-height: 30px;
            }
            .social {
                .item {
                    display: flex;
                    justify-content: space-between;
                    font-size: 15px;
                    line-height: 38px;
                    span {
                        width: 50%;
                    }
                }
            }
            .education {
                .item {
                    display: flex;
                    justify-content: space-between;
                    font-size: 15px;
                    line-height: 38px;
                    span {
                        width: 33.3%;
                    }
                }
            }
          }
        }
      }
    }
  }
}
</style>