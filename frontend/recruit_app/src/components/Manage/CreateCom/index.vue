<template>
  <div class="create-company">
    <div class="container">
      <header>创建公司主页</header>
      <div class="com-form">
        <el-form ref="form" :model="company" label-width="100px">
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label-width="0">
                  <el-alert
                    title="* 为必填项，信息可参考天眼查"
                    type="warning">
                  </el-alert>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <div class="grid-content">
                <el-form-item label="公司Logo"  :rules="[{ required: true }]">
                  <el-upload
                    class="avatar-uploader"
                    action="https://upload.qiniup.com"
                    :data="token"
                    :show-file-list="false"
                    :on-success="handleCompanyLogoSuccess"
                  >
                    <img v-if="company.companyLogo" :src="company.companyLogo" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="16">
              <el-form-item label="公司全称" :rules="[{ required: true }]">
                  <el-input v-model="company.companyFullName"></el-input>
              </el-form-item>
              <el-form-item label="公司简称" :rules="[{ required: true }]">
                  <el-input v-model="company.companyShortName"></el-input>
              </el-form-item>
              <el-form-item label="公司规模" :rules="[{ required: true }]">
                <el-select v-model="company.companySize" placeholder="请选择公司规模" style="width:100%">
                  <el-option v-for="(item, i) in companySize" :key="i" :label="item.label" :value="item.value"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label="经营范围" :rules="[{ required: true }]">
                  <el-input type="textarea" v-model="company.industryField"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label="公司签名" :rules="[{ required: true }]">
                  <el-input type="textarea" v-model="company.signature"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label="公司介绍" :rules="[{ required: true }]">
                  <mavon-editor 
                    :subfield=false
                    :ishljs = "true"
                    boxShadowStyle="0px 0px 0px 1px rgb(221, 223, 231)"
                    v-model="company.companyIntro" 
                    ref=md @imgAdd="imgAdd"
                    :toolbars="toolbars"
                    @save="createCompany"
                    placeholder="点击全屏实时预览"
                    style="min-height:500px"
                    >
                  </mavon-editor>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label="公司标签" :rules="[{ required: true }]">
                  <el-tag
                    :key="tag"
                    v-for="tag in company.companyLabelList"
                    closable
                    :disable-transitions="false"
                    @close="handleClose('companyLabelList',tag)">
                    {{tag}}
                  </el-tag>
                  <el-input
                    class="input-new-tag"
                    v-if="companyLabelListInput"
                    v-model="companyLabelListValue"
                    ref="saveCompanyLabelListInput"
                    size="small"
                    @keyup.enter.native="handleInputConfirm('companyLabelList')"
                    @blur="handleInputConfirm('companyLabelList')"
                  >
                  </el-input>
                  <el-button v-else class="button-new-tag" size="small" @click="showInput('companyLabelList')">+ 添加</el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <div class="grid-content">
                <el-form-item label="营业执照" :rules="[{ required: true }]">
                  <el-upload
                    class="avatar-uploader"
                    action="https://upload.qiniup.com"
                    :data="token"
                    :show-file-list="false"
                    :on-success="handleBusinessLicenseSuccess"
                  >
                    <img v-if="company.businessLicense" :src="company.businessLicense" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="16">
              <div class="grid-content">
                <el-form-item label="注册资金" :rules="[{ required: true }]">
                  <el-input v-model="company.capital" placeholder="单位：万人民币"></el-input>
                </el-form-item>
                <el-form-item label="法人代表" :rules="[{ required: true }]">
                  <el-input v-model="company.legalRepresentative"></el-input>
                </el-form-item>
                <el-form-item label="公司首页" :rules="[{ required: true }]">
                  <el-input v-model="company.companySite"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <div class="grid-content">
                <el-form-item label="融资情况" :rules="[{ required: true }]">
                  <el-input v-model="company.financeStage"></el-input>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="grid-content">
                <el-form-item label="成立时间" :rules="[{ required: true }]">
                  <el-date-picker
                    style="width: 100%"
                    v-model="company.createTime"
                    type="date"
                    placeholder="选择日期">
                  </el-date-picker>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label="公司位置" :rules="[{ required: true }]">
                  <el-input id="pickerInput" v-model="company.companyAddress" placeholder="请输入地址"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item>
                  <div id="container"></div>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div class="grid-content">
                <el-form-item label="员工邮箱">
                  <el-tag
                    :key="tag"
                    v-for="tag in company.companyEmail"
                    closable
                    :disable-transitions="false"
                    @close="handleClose('companyEmail', tag)">
                    {{tag}}
                  </el-tag>
                  <el-input
                    class="input-new-tag"
                    v-if="companyEmailInput"
                    v-model="companyEmailValue"
                    ref="saveCompanyEmailInput"
                    size="small"
                    @keyup.enter.native="handleInputConfirm('companyEmail')"
                    @blur="handleInputConfirm('companyEmail')"
                  >
                  </el-input>
                  <el-button v-else class="button-new-tag" size="small" @click="showInput('companyEmail')">+ 添加</el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
          <el-divider content-position="left">创始人信息</el-divider>
          <el-row>
            <el-col :span="8">
              <div class="grid-content">
                <el-form-item label="头像" :rules="[{ required: true }]">
                  <el-upload
                    class="avatar-uploader"
                    action="https://upload.qiniup.com"
                    :data="token"
                    :show-file-list="false"
                    :on-success="handleCreatePersonAvatarSuccess"
                  >
                    <img v-if="company.createPersonAvatar" :src="company.createPersonAvatar" class="avatar">
                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  </el-upload>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="16">
              <div class="grid-content">
                <el-form-item label="姓名" :rules="[{ required: true }]">
                  <el-input type="text" v-model="company.createPerson"></el-input>
                </el-form-item>
                <el-form-item label="简介" :rules="[{ required: true }]">
                  <el-input type="textarea" v-model="company.createPersonIntro"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
        <div class="operate">
            <a href="javascript:;" @click="createCompany">发表</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  data() {
    return {
      token: {},
      user_id: '',
      company: {
        companyFullName: "",
        companyShortName: "",
        companySize: "",
        companyLogo: "",
        industryField: "",
        companyLabelList: [],
        businessLicense: "",
        capital: "",
        legalRepresentative: "",
        companySite: "",
        signature: "",
        companyIntro: "",
        companyIntroHtml: "",
        financeStage: "",
        createTime: "",
        companyEmail: [],
        createPersonAvatar: "",
        createPerson: "",
        createPersonIntro: "",
        companyAddress: "",
        latitude: "",
        longitude: "",
        creator: sessionStorage.user_id,
      },
      companySize: [
        {value:0, label: '15-50'},
        {value:1, label: '50-150'},
        {value:2, label: '150-500'},
        {value:3, label: '500-2000'},
        {value:4, label: '2000以上'}
      ],
      companyLabelListInput: false,
      companyEmailInput: false,
      companyLabelListValue: '',
      companyEmailValue: '',
      toolbars: this.settings.toolbars
    };
  },
  watch: {
    "company.companyIntro" () {
      this.company.companyIntroHtml = this.$refs.md.d_render;
    },
  },
  created () {
    this.user_id = sessionStorage.user_id;
    this.get_token();
    this.getPosition();
  },
  methods: {
    // 获取token
    async get_token() {
      let res = await this.axios.get(`${this.settings.Host}/avatar/`);
      this.token = res.data;
    },
    // 上传头像成功后的操作
    handleCompanyLogoSuccess (res, file) {
      this.company.companyLogo = "http://q7t570ec4.bkt.clouddn.com/" + res.key
      this.get_token();
    },
    handleBusinessLicenseSuccess (res, file) {
      this.company.businessLicense = "http://q7t570ec4.bkt.clouddn.com/" + res.key
      this.get_token();
    },
    handleCreatePersonAvatarSuccess (res, file) {
      this.company.createPersonAvatar = "http://q7t570ec4.bkt.clouddn.com/" + res.key
      this.get_token();
    },
    handleClose(field, tag) {
      // 移除标签
      if (field == 'companyLabelList') {
        this.company.companyLabelList.splice(this.company.companyLabelList.indexOf(tag), 1);
      } else if (field == 'companyEmail') {
        this.company.companyEmail.splice(this.company.companyEmail.indexOf(tag), 1);
      }
    },
    showInput(field) {
      if (field == 'companyLabelList') {
        this.companyLabelListInput = true;
        this.$nextTick(_ => {
          this.$refs.saveCompanyLabelListInput.$refs.input.focus();
        });
      } else if (field == 'companyEmail') {
        this.companyEmailInput = true;
        this.$nextTick(_ => {
          this.$refs.saveCompanyEmailInput.$refs.input.focus();
        });
      }

    },
    handleInputConfirm(field) {
      if (field == 'companyLabelList') {
        let companyLabelListValue = this.companyLabelListValue;
        if (companyLabelListValue) {
          this.company.companyLabelList.push(companyLabelListValue);
        }
        this.companyLabelListInput = false;
        this.companyLabelListValue = '';
      } else if (field == 'companyEmail') {
        let companyEmailValue = this.companyEmailValue;
        if (companyEmailValue) {
          this.company.companyEmail.push(companyEmailValue);
        }
        this.companyEmailInput = false;
        this.companyEmailValue = '';
      }
    },
    // 地理编码
    poiPickerReady (poiPicker, map) {
      window.poiPicker = poiPicker;
      var marker = new AMap.Marker();
      var infoWindow = new AMap.InfoWindow({
          offset: new AMap.Pixel(0, -20)
      });
      //选取了某个POI
      poiPicker.on('poiPicked', (poiResult => {
        var source = poiResult.source,
        poi = poiResult.item,
        info = {
            source: source,
            id: poi.id,
            name: poi.name,
            location: poi.location.toString(),
            address: poi.address
        };
        marker.setMap(map);
        infoWindow.setMap(map);
        marker.setPosition(poi.location);
        infoWindow.setPosition(poi.location);
        let address = info.name +""+info.address;
        infoWindow.setContent(address);
        this.companyAddress = address;
        this.address = info.name;
        let new_info = info.location.split(',');
        this.company.longitude = new_info[0];
        this.company.latitude = new_info[1];
        infoWindow.open(map, marker.getPosition());
        map.setCenter(marker.getPosition());
      }));
    },
    getPosition () {
      AMapUI.loadUI(['misc/PoiPicker'], (PoiPicker => {
        let map = new AMap.Map('container', {
          zoom: 10
        });
        let poiPicker = new PoiPicker({
            //city:'北京',
            input: 'pickerInput'
        });
        //初始化poiPicker
        this.poiPickerReady(poiPicker, map)
      }));
    },
    // 绑定@imgAdd event
    imgAdd(pos, $file){
        // 第一步.将图片上传到服务器.
        var formdata = new FormData();
        formdata.append('image', $file);
        axios({
            url: 'http://api.offend.com:8000/avatar/',
            method: 'post',
            data: formdata,
            headers: { 'Content-Type': 'multipart/form-data' },
        }).then((url) => {
            // 第二步.将返回的url替换到文本原位置![...](./0) -> ![...](url)
            /**
         * $vm 指为mavonEditor实例，可以通过如下两种方式获取
         * 1. 通过引入对象获取: `import {mavonEditor} from ...` 等方式引入后，`$vm`为`mavonEditor`
         * 2. 通过$refs获取: html声明ref : `<mavon-editor ref=md ></mavon-editor>，`$vm`为 `this.$refs.md`
         */
            $vm.$img2Url(pos, url);
        })
    },
    createCompany () {
      let that = this
      this.axios.post(`${this.settings.Host}/home/company/retrieve/`, {
        companyId: Date.parse(new Date()),
        companyFullName: this.company.companyFullName,
        companyShortName: this.company.companyShortName,
        companySize: Number(this.company.companySize),
        companyLogo: this.company.companyLogo,
        industryField: this.company.industryField,
        companyLabelList: this.company.companyLabelList.join('|'),
        businessLicense: this.company.businessLicense,
        capital: Number(this.company.capital),
        legalRepresentative: this.company.legalRepresentative,
        companySite: this.company.companySite,
        signature: this.company.signature,
        companyIntro: this.company.companyIntro,
        companyIntroHtml: this.company.companyIntroHtml,
        financeStage: this.company.financeStage,
        createTime: moment(this.company.createTime).format("YYYY-MM-DD"),
        companyEmail: this.company.companyEmail.join('|'),
        createPersonAvatar: this.company.createPersonAvatar,
        createPerson: this.company.createPerson,
        createPersonIntro: this.company.createPersonIntro,
        latitude: this.company.latitude,
        longitude: this.company.longitude,
        creator: sessionStorage.user_id,
        orders: 1,
      })
      .then(response => {
          this.$notify({
              title: '成功',
              message: '创建成功，等待审核',
              type: 'success'
          });
      }).catch(error => {
          this.$notify({
              title: '失败',
              message: '请检查是否有空白选项',
              type: 'error'
          });
      })
    }
  }
}
</script>

<style lang="less" rel="stylesheet/less">
.create-company {
  background-color: #f6f6f6;
  .container {
    header {
      width: 840px;
      margin: 0 auto;
      padding: 20px 0;
      font-size: 32px;
      color: #333;
    }
    .com-form {
      margin: 0 auto 20px;
      padding: 20px;
      width: 840px;
      box-sizing: border-box;
      background-color: #fff;
      border-radius: 10px;
      margin-bottom: 20px;
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
      .el-form {
        .el-row {
          .el-col {
            .grid-content {
              #container {
                width: 100%;
                height: 300px;
              }
              .el-form-item {
                .avatar-uploader .el-upload {
                  border: 1px dashed #d9d9d9;
                  border-radius: 6px;
                  cursor: pointer;
                  position: relative;
                  overflow: hidden;
                }
                .avatar-uploader .el-upload:hover {
                  border-color: #409EFF;
                }
                .avatar-uploader-icon {
                  font-size: 28px;
                  color: #8c939d;
                  width: 178px;
                  height: 178px;
                  line-height: 178px;
                  text-align: center;
                }
                .avatar {
                  width: 178px;
                  height: 178px;
                  display: block;
                }
                .el-tag + .el-tag {
                  margin-left: 10px;
                }
                .button-new-tag {
                  margin-left: 10px;
                  height: 32px;
                  line-height: 30px;
                  padding-top: 0;
                  padding-bottom: 0;
                }
                .input-new-tag {
                  width: 90px;
                  margin-left: 10px;
                  vertical-align: bottom;
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