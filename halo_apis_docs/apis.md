# Halo API 接口文档

## 📚 概述

**Halo 版本**: 2.21.7  
**API 规范**: OpenAPI 3.0.1  
**服务器地址**: http://localhost:8091  
**认证方式**: Basic Auth 和 Bearer Token

Halo 的 API 文档分为 **4 个主要模块**:

1. **Console API** - 后台管理控制台 API
2. **Extension API** - 扩展系统核心资源管理 API
3. **Public API** - 公开访问的前台 API
4. **User Center API** - 用户中心个人管理 API

---

## 🔧 1. Console API

### 基本信息
- **文档文件**: `apis_console.json`
- **用途**: 后台管理控制台 API
- **基础路径**: `/apis/api.console.halo.run/v1alpha1`

### 1.1 附件管理 (AttachmentV1alpha1Console)

#### 搜索附件
```
GET /apis/api.console.halo.run/v1alpha1/attachments
```

**查询参数**:
- `page` (integer): 页码，默认为 0
- `size` (integer): 每页大小，默认为 0
- `labelSelector` (array): 标签选择器，如 `hidden!=true`
- `fieldSelector` (array): 字段选择器，如 `metadata.name==halo`
- `sort` (array): 排序条件，格式: `property,(asc|desc)`
- `ungrouped` (boolean): 过滤未分组的附件
- `keyword` (string): 搜索关键词
- `accepts` (array): 可接受的媒体类型

**响应**: `AttachmentList`

#### 上传附件
```
POST /apis/api.console.halo.run/v1alpha1/attachments/upload
```

**请求体**: `multipart/form-data` - `IUploadRequest`

**响应**: `Attachment`

#### 从 URL 上传附件
```
POST /apis/api.console.halo.run/v1alpha1/attachments/-/upload-from-url
```

**请求体**: `application/json` - `UploadFromUrlRequest`

**响应**: `Attachment`

---

### 1.2 认证提供者管理 (AuthProviderV1alpha1Console)

#### 列出所有认证提供者
```
GET /apis/api.console.halo.run/v1alpha1/auth-providers
```

**描述**: 列出所有认证提供者

**响应**: `ListedAuthProvider[]`

#### 启用认证提供者
```
PUT /apis/api.console.halo.run/v1alpha1/auth-providers/{name}/enable
```

**路径参数**:
- `name` (string, required): 认证提供者名称

**响应**: `AuthProvider`

#### 禁用认证提供者
```
PUT /apis/api.console.halo.run/v1alpha1/auth-providers/{name}/disable
```

**路径参数**:
- `name` (string, required): 认证提供者名称

**响应**: `AuthProvider`

---

### 1.3 评论管理 (CommentV1alpha1Console)

#### 列出评论
```
GET /apis/api.console.halo.run/v1alpha1/comments
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件
- `keyword` (string): 按关键词过滤评论
- `ownerKind` (string): 评论者类型
- `ownerName` (string): 评论者名称

**响应**: `ListedCommentList`

#### 创建评论
```
POST /apis/api.console.halo.run/v1alpha1/comments
```

**请求体**: `application/json` - `CommentRequest`

**响应**: `Comment`

#### 创建回复
```
POST /apis/api.console.halo.run/v1alpha1/comments/{name}/reply
```

**路径参数**:
- `name` (string, required): 评论名称

**请求体**: `application/json` - `ReplyRequest`

**响应**: `Reply`

---

### 1.4 索引管理 (IndicesV1alpha1Console)

#### 重建所有索引
```
POST /apis/api.console.halo.run/v1alpha1/indices/-/rebuild
```

**描述**: 重建所有索引

---

### 1.5 通知器管理 (NotifierV1alpha1Console)

#### 获取发送者配置
```
GET /apis/api.console.halo.run/v1alpha1/notifiers/{name}/sender-config
```

**路径参数**:
- `name` (string, required): 通知器名称

**响应**: `object`

#### 保存发送者配置
```
POST /apis/api.console.halo.run/v1alpha1/notifiers/{name}/sender-config
```

**路径参数**:
- `name` (string, required): 通知器名称

**请求体**: `application/json` - `object`

---

### 1.6 插件管理 (PluginV1alpha1Console)

#### 列出插件
```
GET /apis/api.console.halo.run/v1alpha1/plugins
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件
- `keyword` (string): 插件名称或描述关键词
- `enabled` (boolean): 插件是否启用

**响应**: `PluginList`

#### 安装插件（上传 JAR）
```
POST /apis/api.console.halo.run/v1alpha1/plugins/install
```

**描述**: 通过上传 Jar 文件安装插件

**请求体**: `multipart/form-data` - `PluginInstallRequest`

**响应**: `Plugin`

#### 从 URI 安装插件
```
POST /apis/api.console.halo.run/v1alpha1/plugins/-/install-from-uri
```

**请求体**: `application/json` - `InstallFromUriRequest`

**响应**: `Plugin`

#### 升级插件（上传 JAR）
```
POST /apis/api.console.halo.run/v1alpha1/plugins/{name}/upgrade
```

**路径参数**:
- `name` (string, required): 插件名称

**请求体**: `multipart/form-data` - `PluginInstallRequest`

#### 从 URI 升级插件
```
POST /apis/api.console.halo.run/v1alpha1/plugins/{name}/upgrade-from-uri
```

**路径参数**:
- `name` (string, required): 插件名称

**请求体**: `application/json` - `UpgradeFromUriRequest`

**响应**: `Plugin`

#### 更改插件运行状态
```
PUT /apis/api.console.halo.run/v1alpha1/plugins/{name}/plugin-state
```

**路径参数**:
- `name` (string, required): 插件名称

**请求体**: `application/json` - `PluginRunningStateRequest`

**响应**: `Plugin`

#### 重载插件
```
PUT /apis/api.console.halo.run/v1alpha1/plugins/{name}/reload
```

**路径参数**:
- `name` (string, required): 插件名称

**响应**: `Plugin`

#### 获取插件 JSON 配置
```
GET /apis/api.console.halo.run/v1alpha1/plugins/{name}/json-config
```

**路径参数**:
- `name` (string, required): 插件名称

**描述**: 获取通过配置的 configMapName 转换的 JSON 配置

**响应**: `object`

#### 更新插件 JSON 配置
```
PUT /apis/api.console.halo.run/v1alpha1/plugins/{name}/json-config
```

**路径参数**:
- `name` (string, required): 插件名称

**请求体**: `application/json` - `object`

**响应**: 204 No Content

#### 重置插件配置
```
PUT /apis/api.console.halo.run/v1alpha1/plugins/{name}/reset-config
```

**路径参数**:
- `name` (string, required): 插件名称

**响应**: `ConfigMap`

#### 获取插件设置
```
GET /apis/api.console.halo.run/v1alpha1/plugins/{name}/setting
```

**路径参数**:
- `name` (string, required): 插件名称

**响应**: `Setting`

#### 获取合并的 CSS 包
```
GET /apis/api.console.halo.run/v1alpha1/plugins/-/bundle.css
```

**描述**: 将所有已启用插件的 CSS 包合并为一个

**响应**: `string`

#### 获取合并的 JS 包
```
GET /apis/api.console.halo.run/v1alpha1/plugins/-/bundle.js
```

**描述**: 将所有已启用插件的 JS 包合并为一个

**响应**: `string`

---

### 1.7 文章管理 (PostV1alpha1Console)

#### 列出文章
```
GET /apis/api.console.halo.run/v1alpha1/posts
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: 文章列表

---

## 🔌 2. Extension API

### 基本信息
- **文档文件**: `apis_extension.json`
- **用途**: 扩展系统核心资源管理 API
- **基础路径**: `/api/v1alpha1`

### 2.1 资源类型

Extension API 提供了标准的 CRUD 操作来管理以下资源:

- **AnnotationSetting** - 注解设置
- **ConfigMap** - 配置映射
- **MenuItem** - 菜单项
- **Menu** - 菜单
- **RoleBinding** - 角色绑定

### 2.2 标准操作模式

每个资源都支持以下标准操作:

#### 列表查询
```
GET /api/v1alpha1/{resource}
```

**查询参数**:
- `page` (integer): 页码，默认为 0
- `size` (integer): 每页大小，默认为 0
- `labelSelector` (array): 标签选择器，如 `hidden!=true`
- `fieldSelector` (array): 字段选择器，如 `metadata.name==halo`
- `sort` (array): 排序条件，格式: `property,(asc|desc)`

**响应**: `{Resource}List`

#### 创建资源
```
POST /api/v1alpha1/{resource}
```

**请求体**: 资源对象

**响应**: 创建的资源对象

#### 获取单个资源
```
GET /api/v1alpha1/{resource}/{name}
```

**路径参数**:
- `name` (string, required): 资源名称

**响应**: 资源对象

#### 更新资源
```
PUT /api/v1alpha1/{resource}/{name}
```

**路径参数**:
- `name` (string, required): 资源名称

**请求体**: 更新后的资源对象

**响应**: 更新后的资源对象

#### 部分更新资源（JSON Patch）
```
PATCH /api/v1alpha1/{resource}/{name}
```

**路径参数**:
- `name` (string, required): 资源名称

**请求体**: `application/json-patch+json` - `JsonPatch`

**响应**: 更新后的资源对象

#### 删除资源
```
DELETE /api/v1alpha1/{resource}/{name}
```

**路径参数**:
- `name` (string, required): 资源名称

**响应**: 200 OK

---

### 2.3 具体资源端点

#### AnnotationSetting（注解设置）
- `GET /api/v1alpha1/annotationsettings`
- `POST /api/v1alpha1/annotationsettings`
- `GET /api/v1alpha1/annotationsettings/{name}`
- `PUT /api/v1alpha1/annotationsettings/{name}`
- `PATCH /api/v1alpha1/annotationsettings/{name}`
- `DELETE /api/v1alpha1/annotationsettings/{name}`

#### ConfigMap（配置映射）
- `GET /api/v1alpha1/configmaps`
- `POST /api/v1alpha1/configmaps`
- `GET /api/v1alpha1/configmaps/{name}`
- `PUT /api/v1alpha1/configmaps/{name}`
- `PATCH /api/v1alpha1/configmaps/{name}`
- `DELETE /api/v1alpha1/configmaps/{name}`

#### MenuItem（菜单项）
- `GET /api/v1alpha1/menuitems`
- `POST /api/v1alpha1/menuitems`
- `GET /api/v1alpha1/menuitems/{name}`
- `PUT /api/v1alpha1/menuitems/{name}`
- `PATCH /api/v1alpha1/menuitems/{name}`
- `DELETE /api/v1alpha1/menuitems/{name}`

#### Menu（菜单）
- `GET /api/v1alpha1/menus`
- `POST /api/v1alpha1/menus`
- `GET /api/v1alpha1/menus/{name}`
- `PUT /api/v1alpha1/menus/{name}`
- `PATCH /api/v1alpha1/menus/{name}`
- `DELETE /api/v1alpha1/menus/{name}`

#### RoleBinding（角色绑定）
- `GET /api/v1alpha1/rolebindings`
- `POST /api/v1alpha1/rolebindings`
- `GET /api/v1alpha1/rolebindings/{name}`
- `PUT /api/v1alpha1/rolebindings/{name}`
- `PATCH /api/v1alpha1/rolebindings/{name}`
- `DELETE /api/v1alpha1/rolebindings/{name}`

---

## 🌐 3. Public API

### 基本信息
- **文档文件**: `apis_public.json`
- **用途**: 公开访问的前台 API
- **基础路径**: `/apis/api.content.halo.run/v1alpha1` 或 `/apis/api.halo.run/v1alpha1`

### 3.1 分类管理 (CategoryV1alpha1Public)

#### 列出分类
```
GET /apis/api.content.halo.run/v1alpha1/categories
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `CategoryVoList`

#### 按名称获取分类
```
GET /apis/api.content.halo.run/v1alpha1/categories/{name}
```

**路径参数**:
- `name` (string, required): 分类名称

**响应**: `CategoryVo`

#### 按分类名称列出文章
```
GET /apis/api.content.halo.run/v1alpha1/categories/{name}/posts
```

**路径参数**:
- `name` (string, required): 分类名称

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `ListedPostVoList`

---

### 3.2 文章管理 (PostV1alpha1Public)

#### 列出文章
```
GET /apis/api.content.halo.run/v1alpha1/posts
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `ListedPostVoList`

#### 按名称获取文章
```
GET /apis/api.content.halo.run/v1alpha1/posts/{name}
```

**路径参数**:
- `name` (string, required): 文章名称

**响应**: `PostVo`

#### 获取文章导航
```
GET /apis/api.content.halo.run/v1alpha1/posts/{name}/navigation
```

**描述**: 获取文章的上一篇/下一篇导航信息

**路径参数**:
- `name` (string, required): 文章名称

**响应**: `NavigationPostVo`

---

### 3.3 独立页面 (SinglePageV1alpha1Public)

#### 列出独立页面
```
GET /apis/api.content.halo.run/v1alpha1/singlepages
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `ListedSinglePageVoList`

#### 按名称获取独立页面
```
GET /apis/api.content.halo.run/v1alpha1/singlepages/{name}
```

**路径参数**:
- `name` (string, required): 独立页面名称

**响应**: `SinglePageVo`

---

### 3.4 标签管理 (TagV1alpha1Public)

#### 列出标签
```
GET /apis/api.content.halo.run/v1alpha1/tags
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `TagVoList`

#### 按名称获取标签
```
GET /apis/api.content.halo.run/v1alpha1/tags/{name}
```

**路径参数**:
- `name` (string, required): 标签名称

**响应**: `TagVo`

#### 按标签名称列出文章
```
GET /apis/api.content.halo.run/v1alpha1/tags/{name}/posts
```

**路径参数**:
- `name` (string, required): 标签名称

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `ListedPostVo`

---

### 3.5 评论系统 (CommentV1alpha1Public)

#### 列出评论
```
GET /apis/api.halo.run/v1alpha1/comments
```

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `sort` (array): 排序条件
- `group` (string): 评论主体分组
- `version` (string, required): 评论主体版本
- `kind` (string, required): 评论主体类型
- `name` (string, required): 评论主体名称
- `withReplies` (boolean): 是否包含回复，默认 false
- `replySize` (integer): 回复数量，默认 10，仅在 withReplies 为 true 时有效

**响应**: `CommentWithReplyVoList`

#### 创建评论
```
POST /apis/api.halo.run/v1alpha1/comments
```

**请求体**: `application/json` - `CommentRequest`

**响应**: `Comment`

#### 获取评论
```
GET /apis/api.halo.run/v1alpha1/comments/{name}
```

**路径参数**:
- `name` (string, required): 评论名称

**响应**: `CommentVoList`

#### 列出评论回复
```
GET /apis/api.halo.run/v1alpha1/comments/{name}/reply
```

**路径参数**:
- `name` (string, required): 评论名称

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小

**响应**: `ReplyVoList`

#### 创建回复
```
POST /apis/api.halo.run/v1alpha1/comments/{name}/reply
```

**路径参数**:
- `name` (string, required): 评论名称

**请求体**: `application/json` - `ReplyRequest`

**响应**: `Reply`

---

### 3.6 搜索功能 (IndexV1alpha1Public)

#### 搜索索引
```
POST /apis/api.halo.run/v1alpha1/indices/-/search
```

**描述**: 搜索索引。注意：此端点忽略 "filterPublished"、"filterExposed" 和 "filterRecycled" 字段。

**请求体**: `SearchOption`

**响应**: `SearchResult`

---

### 3.7 菜单系统 (MenuV1alpha1Public)

#### 获取主菜单
```
GET /apis/api.halo.run/v1alpha1/menus/-
```

**响应**: `MenuVo`

#### 按名称获取菜单
```
GET /apis/api.halo.run/v1alpha1/menus/{name}
```

**路径参数**:
- `name` (string, required): 菜单名称

**响应**: `MenuVo`

---

### 3.8 站点统计 (SystemV1alpha1Public)

#### 获取站点统计
```
GET /apis/api.halo.run/v1alpha1/stats/-
```

**响应**: `SiteStatsVo`

---

### 3.9 访问跟踪

#### 计数器跟踪
```
POST /apis/api.halo.run/v1alpha1/trackers/counter
```

**描述**: 记录访问计数

---

## 👤 4. User Center API

### 基本信息
- **文档文件**: `apis_uc.json`
- **用途**: 用户中心个人管理 API
- **基础路径**: 
  - `/apis/api.notification.halo.run/v1alpha1`
  - `/apis/uc.api.auth.halo.run/v1alpha1`
  - `/apis/uc.api.content.halo.run/v1alpha1`
  - `/apis/uc.api.halo.run/v1alpha1`
  - `/apis/uc.api.security.halo.run/v1alpha1`

### 4.1 通知管理 (NotificationV1alpha1Uc)

#### 获取通知器接收者配置
```
GET /apis/api.notification.halo.run/v1alpha1/notifiers/{name}/receiver-config
```

**路径参数**:
- `name` (string, required): 通知器名称

**响应**: `object`

#### 保存通知器接收者配置
```
POST /apis/api.notification.halo.run/v1alpha1/notifiers/{name}/receiver-config
```

**路径参数**:
- `name` (string, required): 通知器名称

**请求体**: `application/json` - `object`

#### 列出用户通知偏好
```
GET /apis/api.notification.halo.run/v1alpha1/userspaces/{username}/notification-preferences
```

**路径参数**:
- `username` (string, required): 用户名

**响应**: `ReasonTypeNotifierMatrix`

#### 保存用户通知偏好
```
POST /apis/api.notification.halo.run/v1alpha1/userspaces/{username}/notification-preferences
```

**路径参数**:
- `username` (string, required): 用户名

**请求体**: `ReasonTypeNotifierCollectionRequest`

**响应**: `ReasonTypeNotifierMatrix`

#### 列出用户通知
```
GET /apis/api.notification.halo.run/v1alpha1/userspaces/{username}/notifications
```

**路径参数**:
- `username` (string, required): 用户名

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件

**响应**: `NotificationList`

#### 标记指定通知为已读
```
PUT /apis/api.notification.halo.run/v1alpha1/userspaces/{username}/notifications/-/mark-specified-as-read
```

**路径参数**:
- `username` (string, required): 用户名

**请求体**: `application/json` - `MarkSpecifiedRequest`

**响应**: `string[]` (已标记的通知名称列表)

#### 标记单个通知为已读
```
PUT /apis/api.notification.halo.run/v1alpha1/userspaces/{username}/notifications/{name}/mark-as-read
```

**路径参数**:
- `username` (string, required): 用户名
- `name` (string, required): 通知名称

**响应**: `Notification`

#### 删除指定通知
```
DELETE /apis/api.notification.halo.run/v1alpha1/userspaces/{username}/notifications/{name}
```

**路径参数**:
- `username` (string, required): 用户名
- `name` (string, required): 通知名称

**响应**: `Notification`

---

### 4.2 第三方账号连接 (UserConnectionV1alpha1Uc)

#### 断开我的第三方平台连接
```
PUT /apis/uc.api.auth.halo.run/v1alpha1/user-connections/{registerId}/disconnect
```

**路径参数**:
- `registerId` (string, required): 第三方平台的注册 ID

**响应**: `UserConnection[]`

---

### 4.3 我的文章管理 (PostV1alpha1Uc)

#### 列出我的文章
```
GET /apis/uc.api.content.halo.run/v1alpha1/posts
```

**描述**: 列出当前用户拥有的文章

**查询参数**:
- `page` (integer): 页码
- `size` (integer): 每页大小
- `labelSelector` (array): 标签选择器
- `fieldSelector` (array): 字段选择器
- `sort` (array): 排序条件
- `publishPhase` (enum): 按发布阶段过滤
  - `DRAFT` - 草稿
  - `PENDING_APPROVAL` - 待审核
  - `PUBLISHED` - 已发布
  - `FAILED` - 失败
- `keyword` (string): 按关键词过滤
- `categoryWithChildren` (string): 按分类过滤（包含子分类）

**响应**: `ListedPostList`

#### 创建我的文章
```
POST /apis/uc.api.content.halo.run/v1alpha1/posts
```

**描述**: 创建我的文章。如果要创建包含内容的文章，请在注解中设置 "content.halo.run/content-json" 并参考 Content 数据类型。

**请求体**: `Post`

**响应**: `Post`

#### 获取我的文章
```
GET /apis/uc.api.content.halo.run/v1alpha1/posts/{name}
```

**描述**: 获取属于当前用户的文章

**路径参数**:
- `name` (string, required): 文章名称

**响应**: `Post`

#### 更新我的文章
```
PUT /apis/uc.api.content.halo.run/v1alpha1/posts/{name}
```

**路径参数**:
- `name` (string, required): 文章名称

**请求体**: `Post`

**响应**: `Post`

#### 获取我的文章草稿
```
GET /apis/uc.api.content.halo.run/v1alpha1/posts/{name}/draft
```

**路径参数**:
- `name` (string, required): 文章名称

**查询参数**:
- `patched` (boolean): 是否包含补丁内容和原始内容

**响应**: `Snapshot`

#### 更新我的文章草稿
```
PUT /apis/uc.api.content.halo.run/v1alpha1/posts/{name}/draft
```

**描述**: 更新我的文章草稿。请确保在注解中设置 "content.halo.run/content-json" 并参考 Content 数据类型。

**路径参数**:
- `name` (string, required): 文章名称

**请求体**: `Snapshot`

**响应**: `Snapshot`

#### 发布我的文章
```
PUT /apis/uc.api.content.halo.run/v1alpha1/posts/{name}/publish
```

**路径参数**:
- `name` (string, required): 文章名称

**响应**: `Post`

#### 取消发布我的文章
```
PUT /apis/uc.api.content.halo.run/v1alpha1/posts/{name}/unpublish
```

**路径参数**:
- `name` (string, required): 文章名称

**响应**: `Post`

#### 将我的文章移至回收站
```
DELETE /apis/uc.api.content.halo.run/v1alpha1/posts/{name}/recycle
```

**路径参数**:
- `name` (string, required): 文章名称

**响应**: `Post`

---

### 4.4 快照管理 (SnapshotV1alpha1Uc)

#### 获取文章快照
```
GET /apis/uc.api.content.halo.run/v1alpha1/snapshots/{name}
```

**路径参数**:
- `name` (string, required): 快照名称

**查询参数**:
- `postName` (string, required): 文章名称
- `patched` (boolean): 是否包含补丁内容和原始内容

**响应**: `Snapshot`

---

### 4.5 用户偏好设置 (UserPreferenceV1alpha1Uc)

#### 按分组获取我的偏好
```
GET /apis/uc.api.halo.run/v1alpha1/user-preferences/{group}
```

**路径参数**:
- `group` (string, required): 用户偏好分组，如 `notification`

**响应**: `JsonNode`

#### 按分组创建或更新我的偏好
```
PUT /apis/uc.api.halo.run/v1alpha1/user-preferences/{group}
```

**路径参数**:
- `group` (string, required): 用户偏好分组，如 `notification`

**请求体**: `JsonNode`

**响应**: 204 No Content (偏好更新成功)

---

### 4.6 双因素认证 (TwoFactorAuthV1alpha1Uc)

#### 获取双因素认证设置
```
GET /apis/uc.api.security.halo.run/v1alpha1/authentications/two-factor/settings
```

**响应**: `TwoFactorAuthSettings`

#### 启用双因素认证
```
PUT /apis/uc.api.security.halo.run/v1alpha1/authentications/two-factor/settings/enabled
```

**请求体**: `PasswordRequest`

**响应**: `TwoFactorAuthSettings`

#### 禁用双因素认证
```
PUT /apis/uc.api.security.halo.run/v1alpha1/authentications/two-factor/settings/disabled
```

**请求体**: `PasswordRequest`

**响应**: `TwoFactorAuthSettings`

#### 配置 TOTP
```
POST /apis/uc.api.security.halo.run/v1alpha1/authentications/two-factor/totp
```

**请求体**: `TotpRequest`

**响应**: `TwoFactorAuthSettings`

---

## 🔑 核心特性

### 1. 统一的查询参数

所有列表 API 都支持以下查询参数:

| 参数 | 类型 | 描述 |
|------|------|------|
| `page` | integer | 页码，默认为 0 |
| `size` | integer | 每页大小，默认为 0 |
| `labelSelector` | array | 标签选择器，如 `hidden!=true` |
| `fieldSelector` | array | 字段选择器，如 `metadata.name==halo` |
| `sort` | array | 排序条件，格式: `property,(asc|desc)`，支持多个排序条件 |

### 2. 认证方式

- **Basic Auth**: HTTP 基本认证
- **Bearer Token**: JWT Token 认证

### 3. RESTful 设计原则

- 遵循 REST 规范
- 使用标准 HTTP 方法:
  - `GET` - 查询资源
  - `POST` - 创建资源
  - `PUT` - 完整更新资源
  - `PATCH` - 部分更新资源（JSON Patch RFC 6902）
  - `DELETE` - 删除资源

### 4. 响应格式

#### 单个资源响应
```json
{
  "metadata": {
    "name": "resource-name",
    "labels": {},
    "annotations": {},
    "creationTimestamp": "2023-01-01T00:00:00Z"
  },
  "spec": {},
  "status": {}
}
```

#### 列表资源响应
```json
{
  "page": 1,
  "size": 20,
  "total": 100,
  "items": [],
  "first": true,
  "last": false,
  "hasNext": true,
  "hasPrevious": false,
  "totalPages": 5
}
```

---

## 📊 数据模型

### 资源结构

所有 Halo 资源都遵循以下结构:

#### Metadata（元数据）
- `name`: 资源名称（唯一标识符）
- `labels`: 标签（key-value 键值对）
- `annotations`: 注解（扩展信息）
- `creationTimestamp`: 创建时间
- `deletionTimestamp`: 删除时间（软删除）
- `version`: 资源版本号

#### Spec（规格）
定义资源的期望状态和配置

#### Status（状态）
反映资源的实际运行状态

---

## 🎯 使用建议

### 1. 分页处理

处理大量数据时务必使用分页参数:

```
GET /apis/api.content.halo.run/v1alpha1/posts?page=0&size=20
```

### 2. 使用选择器精确筛选

#### 标签选择器示例:
```
labelSelector=category=tech&hidden!=true
```

#### 字段选择器示例:
```
fieldSelector=metadata.name==my-post
```

### 3. 排序

支持多个排序条件:
```
sort=metadata.creationTimestamp,desc&sort=metadata.name,asc
```

### 4. 认证最佳实践

- 生产环境使用 Bearer Token
- 定期刷新 Token
- 启用双因素认证（2FA）
- 妥善保管密钥

### 5. 错误处理

API 遵循标准 HTTP 状态码:

| 状态码 | 描述 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 无内容（操作成功） |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 500 | 服务器内部错误 |

### 6. 内容管理注意事项

创建或更新带有内容的文章时，需要在注解中设置:

```json
{
  "metadata": {
    "annotations": {
      "content.halo.run/content-json": "{\"raw\":\"...\",\"content\":\"...\",\"rawType\":\"markdown\"}"
    }
  }
}
```

### 7. JSON Patch 使用

PATCH 操作使用 JSON Patch (RFC 6902) 格式:

```json
[
  {
    "op": "replace",
    "path": "/spec/title",
    "value": "新标题"
  },
  {
    "op": "add",
    "path": "/metadata/labels/new-label",
    "value": "label-value"
  }
]
```

---

## 📝 快速示例

### 示例 1: 获取文章列表（带分页和排序）

```http
GET /apis/api.content.halo.run/v1alpha1/posts?page=0&size=10&sort=metadata.creationTimestamp,desc
Authorization: Bearer <your-token>
```

### 示例 2: 创建评论

```http
POST /apis/api.halo.run/v1alpha1/comments
Authorization: Bearer <your-token>
Content-Type: application/json

{
  "raw": "这是一条评论",
  "content": "<p>这是一条评论</p>",
  "allowNotification": true,
  "subjectRef": {
    "group": "content.halo.run",
    "version": "v1alpha1",
    "kind": "Post",
    "name": "my-post"
  }
}
```

### 示例 3: 按分类查询文章

```http
GET /apis/api.content.halo.run/v1alpha1/categories/tech/posts?page=0&size=20
Authorization: Bearer <your-token>
```

### 示例 4: 发布文章

```http
PUT /apis/uc.api.content.halo.run/v1alpha1/posts/my-post/publish
Authorization: Bearer <your-token>
```

### 示例 5: 搜索内容

```http
POST /apis/api.halo.run/v1alpha1/indices/-/search
Authorization: Bearer <your-token>
Content-Type: application/json

{
  "keyword": "Halo",
  "limit": 10
}
```

---

## 🔗 相关资源

- [Halo 官方文档](https://docs.halo.run)
- [OpenAPI 规范](https://swagger.io/specification/)
- [JSON Patch RFC 6902](https://tools.ietf.org/html/rfc6902)

---

## 📄 许可证

本文档基于 Halo 项目生成，遵循 Halo 项目的许可证。
