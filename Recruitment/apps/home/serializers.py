from rest_framework import serializers
from . import models

class ProvinceSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = ['id', 'name']

class CategorySerializers(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    def get_sub_category(self, obj):
        query_set = obj.sub_category.all()
        sub_dic = []
        for obj in query_set:
            cate = {
                'id': obj.id,
                'name': obj.name,
                'category': obj.category.all().values('id', 'name')
            }
            sub_dic.append(cate)
        return sub_dic

    class Meta:
        model = models.JobBigCategory
        fields = ["id", "name", "sub_category"]

class PositionViewsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        # exclude = ['orders']
        fields = "__all__"

class PositionModelSerializer(serializers.ModelSerializer):
    skillLabels = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()

    def get_skillLabels(self, obj):
        skillLabelList = obj.skillLabels
        return skillLabelList.split(',')

    def get_education(self, obj):
        return obj.get_education_display()

    class Meta:
        model = models.Position
        fields = ['id', 'positionName', 'salary', 'workYear', 'education', 'skillLabels']

class CompanyListSerializer(serializers.ModelSerializer):
    companyLabel = serializers.SerializerMethodField()

    def get_companyLabel (self, obj):
        lst = obj.companyLabelList.split('|')
        return lst

    class Meta:
        model = models.Company
        fields = ['companyId', 'companyLogo', 'companyShortName', 'companyLabel', 'financeStage', 'companyIntro']

class CompanyDetailSerializer(serializers.ModelSerializer):
    companyLabel = serializers.SerializerMethodField()

    def get_companyLabel(self, obj):
        lst = obj.companyLabelList.split('|')
        return lst

    class Meta:
        model = models.Company
        fields = ['companyId', 'companyLogo', 'company_size', 'companySize', 'companyShortName', 'companyFullName', 'industryField', 'financeStage', 'signature', 'companyLabel', 'capital', 'createPerson', 'createPersonIntro', 'companyIntroHtml', 'companySite', 'legalRepresentative', 'createTime', 'createPersonAvatar', 'latitude', 'longitude', 'companyAddress']

class CompanyRetrieveSerializer(serializers.ModelSerializer):
    companyLabelList = serializers.SerializerMethodField()
    company_size = serializers.SerializerMethodField()

    def get_companyLabelList(self, obj):
        return obj.companyLabelList.split('|')

    def get_company_size(self, obj):
        return obj.get_companySize_display()

    class Meta:
        model = models.Company
        fields = ['companyId', 'companyLogo', 'company_size', 'companySize', 'businessLicense', 'companyShortName', 'companyFullName', 'industryField', 'financeStage', 'signature', 'companyLabelList', 'capital', 'createPerson', 'createPersonIntro', 'companyIntro', 'companyIntroHtml', 'companySite', 'legalRepresentative', 'createTime', 'createPersonAvatar', 'latitude', 'longitude', 'companyAddress', 'companyEmail', 'creator', 'is_pass', 'orders', 'message']
        extra_kwargs = {
            "creator": {"write_only": True},
        }

class PositionRetrieveSerializer(serializers.ModelSerializer):
    jobNature = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    publisher = serializers.SerializerMethodField()
    def get_company(self, obj):
        com = models.Company.objects.filter(companyId=obj.companyId).first()
        dic = {}
        dic['companyLogo'] = com.companyLogo
        dic['companyShortName'] = com.companyShortName
        dic['financeStage'] = com.financeStage
        dic['industryField'] = com.industryField
        dic['companySize'] = com.company_size
        dic['companySite'] = com.companySite
        return dic
    
    def get_publisher(self, obj):
        dic = {
            'id': obj.publisher.pk,
            'avatar': obj.publisher.avatar,
            'nic_name': obj.publisher.nic_name
        }
        return dic

    def get_jobNature(self, obj):
        return obj.get_jobNature_display()

    def get_education(self, obj):
        return obj.get_education_display()

    class Meta:
        model = models.Position
        fields = ['positionName', 'salary', 'workYear', 'city', 'district', 'subwayLine', 'stationName', 'education', 'jobNature', 'positionAdvantage', 'positionIntro', 'positionIntroHtml', 'create_time', 'company', 'publisher']
