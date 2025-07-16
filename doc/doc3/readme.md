# ManagPage.vue中，所有叫小程序的，都改成H5网页 ->done
# ManagPage.vue中，去掉“管理”按钮 ->done
# EditPage.vue中，"编辑小程序"改成"编辑H5网页"，“小程序ID”改成"H5网页ID"， “小程序名称”改成“H5网页名称” ->done
# 标题“小程序管理系统”改成“测试管理系统” ->done
# 数据库改造 ->done
   1. 再增加一张表， domain_types, 字段包括：
    id, 
    miniprogram_id
    domain_type

   2. 表 links, 增加一个字段， domain_type
# 数据和网页做关联 ->done
   1. ViewPage.vue中， 展示的链接是： domain_type下的域名 和 link拼接在一起
   2. EditPage.vue中， 域名类型只展示该小程序下的 域名类型
   
# 为什么手动创建就没有中文显示乱码问题， 数据库自己初始化就有问题？？？？

# EditPage.vue, “编辑H5网页”改成对应标题，比如“H5影视-快手”这种的 ->done
