/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 4);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

module.exports = React;

/***/ }),
/* 1 */
/***/ (function(module, exports) {

module.exports = Sentry;

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _react = __webpack_require__(0);

var _react2 = _interopRequireDefault(_react);

var _sentry = __webpack_require__(1);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var IssueActions = function (_plugins$DefaultIssue) {
  _inherits(IssueActions, _plugins$DefaultIssue);

  function IssueActions() {
    _classCallCheck(this, IssueActions);

    return _possibleConstructorReturn(this, (IssueActions.__proto__ || Object.getPrototypeOf(IssueActions)).apply(this, arguments));
  }

  _createClass(IssueActions, [{
    key: 'changeField',
    value: function changeField(action, name, value) {
      var _this2 = this;

      var key = action + 'FormData';
      var formData = _extends({}, this.state[key], _defineProperty({}, name, value));
      var state = _defineProperty({}, key, formData);
      if (name === 'issuetype') {
        state.state = _sentry.FormState.LOADING;
        this.setState(state, this.onLoad.bind(this, function () {
          _this2.api.request(_this2.getPluginCreateEndpoint() + '?issuetype=' + encodeURIComponent(value), {
            success: function success(data) {
              // Try not to change things the user might have edited
              // unless they're no longer valid
              var oldData = _this2.state.createFormData;
              var createFormData = {};
              data.forEach(function (field) {
                var val = void 0;
                if (field.choices && !field.choices.find(function (c) {
                  return c[0] === oldData[field.name];
                })) {
                  val = field.default;
                } else {
                  val = oldData[field.name] || field.default;
                }
                createFormData[field.name] = val;
              });
              _this2.setState({
                createFieldList: data,
                error: null,
                loading: false,
                createFormData: createFormData
              }, _this2.onLoadSuccess);
            },
            error: _this2.errorHandler
          });
        }));
        return;
      }
      this.setState(state);
    }
  }, {
    key: 'renderForm',
    value: function renderForm() {
      var _this3 = this;

      var form = void 0;

      // For create form, split into required and optional fields
      if (this.props.actionType === 'create') {
        if (this.state.createFieldList) {
          var renderField = function renderField(field) {
            if (field.has_autocomplete) {
              field = Object.assign({
                url: '/api/0/issues/' + _this3.getGroup().id + '/plugins/' + _this3.props.plugin.slug + '/autocomplete'
              }, field);
            }
            return _react2.default.createElement(
              'div',
              { key: field.name },
              _this3.renderField({
                config: field,
                formData: _this3.state.createFormData,
                onChange: _this3.changeField.bind(_this3, 'create', field.name)
              })
            );
          };
          var isRequired = function isRequired(f) {
            return f.required != null ? f.required : true;
          };

          var fields = this.state.createFieldList;
          var requiredFields = fields.filter(function (f) {
            return isRequired(f);
          }).map(function (f) {
            return renderField(f);
          });
          var optionalFields = fields.filter(function (f) {
            return !isRequired(f);
          }).map(function (f) {
            return renderField(f);
          });
          form = _react2.default.createElement(
            _sentry.Form,
            { onSubmit: this.createIssue, submitLabel: 'Create Issue', footerClass: '' },
            _react2.default.createElement(
              'h5',
              null,
              'Required Fields'
            ),
            requiredFields,
            optionalFields.length ? _react2.default.createElement(
              'h5',
              null,
              'Optional Fields'
            ) : null,
            optionalFields
          );
        }
      } else {
        form = _get(IssueActions.prototype.__proto__ || Object.getPrototypeOf(IssueActions.prototype), 'renderForm', this).call(this);
      }

      return form;
    }
  }]);

  return IssueActions;
}(_sentry.plugins.DefaultIssuePlugin.DefaultIssueActions);

exports.default = IssueActions;
module.exports = exports['default'];

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = __webpack_require__(0);

var _react2 = _interopRequireDefault(_react);

var _underscore = __webpack_require__(5);

var _underscore2 = _interopRequireDefault(_underscore);

var _sentry = __webpack_require__(1);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Settings = function (_plugins$BasePlugin$D) {
  _inherits(Settings, _plugins$BasePlugin$D);

  function Settings(props) {
    _classCallCheck(this, Settings);

    var _this = _possibleConstructorReturn(this, (Settings.__proto__ || Object.getPrototypeOf(Settings)).call(this, props));

    _this.PAGE_FIELD_LIST = {
      '0': ['instance_url', 'username', 'password'],
      '1': ['default_project'],
      '2': ['ignored_fields', 'default_priority', 'default_issue_type', 'auto_create']
    };

    _this.back = _this.back.bind(_this);
    _this.startEditing = _this.startEditing.bind(_this);
    _this.isLastPage = _this.isLastPage.bind(_this);

    Object.assign(_this.state, {
      page: 0
    });
    return _this;
  }

  _createClass(Settings, [{
    key: 'isConfigured',
    value: function isConfigured(state) {
      state = state || this.state;
      return !!(this.state.formData && this.state.formData.default_project);
    }
  }, {
    key: 'isLastPage',
    value: function isLastPage() {
      return this.state.page === 2;
    }
  }, {
    key: 'fetchData',
    value: function fetchData() {
      var _this2 = this;

      // This is mostly copy paste of parent class
      // except for setting edit state
      this.api.request(this.getPluginEndpoint(), {
        success: function success(data) {
          var formData = {};
          var initialData = {};
          data.config.forEach(function (field) {
            formData[field.name] = field.value || field.defaultValue;
            initialData[field.name] = field.value;
          });
          _this2.setState({
            fieldList: data.config,
            formData: formData,
            initialData: initialData,
            // start off in edit mode if there isn't a project set
            editing: !(formData && formData.default_project)
          }, _this2.onLoadSuccess);
        },
        error: this.onLoadError
      });
    }
  }, {
    key: 'startEditing',
    value: function startEditing() {
      this.setState({ editing: true });
    }
  }, {
    key: 'onSubmit',
    value: function onSubmit() {
      var _this3 = this;

      if (_underscore2.default.isEqual(this.state.initialData, this.state.formData)) {
        if (this.isLastPage()) {
          this.setState({ editing: false, page: 0 });
        } else {
          this.setState({ page: this.state.page + 1 });
        }
        this.onSaveSuccess(this.onSaveComplete);
        return;
      }
      var formData = Object.assign({}, this.state.formData);
      // if the project has changed, it's likely these values aren't valid anymore
      if (formData.default_project !== this.state.initialData.default_project) {
        formData.default_issue_type = null;
        formData.default_priority = null;
      }
      this.api.request(this.getPluginEndpoint(), {
        data: formData,
        method: 'PUT',
        success: this.onSaveSuccess.bind(this, function (data) {
          var formData = {};
          var initialData = {};
          data.config.forEach(function (field) {
            formData[field.name] = field.value || field.defaultValue;
            initialData[field.name] = field.value;
          });
          var state = {
            formData: formData,
            initialData: initialData,
            errors: {},
            fieldList: data.config
          };
          if (_this3.isLastPage()) {
            state.editing = false;
            state.page = 0;
          } else {
            state.page = _this3.state.page + 1;
          }
          _this3.setState(state);
        }),
        error: this.onSaveError.bind(this, function (error) {
          _this3.setState({
            errors: (error.responseJSON || {}).errors || {}
          });
        }),
        complete: this.onSaveComplete
      });
    }
  }, {
    key: 'back',
    value: function back(ev) {
      ev.preventDefault();
      if (this.state.state === _sentry.FormState.SAVING) {
        return;
      }
      this.setState({
        page: this.state.page - 1
      });
    }
  }, {
    key: 'render',
    value: function render() {
      var _this4 = this;

      if (this.state.state === _sentry.FormState.LOADING) {
        return _react2.default.createElement(_sentry.LoadingIndicator, null);
      }

      if (this.state.state === _sentry.FormState.ERROR && !this.state.fieldList) {
        return _react2.default.createElement(
          'div',
          { className: 'alert alert-error m-b-1' },
          'An unknown error occurred. Need help with this? ',
          _react2.default.createElement(
            'a',
            { href: 'https://sentry.io/support/' },
            'Contact support'
          )
        );
      }

      var isSaving = this.state.state === _sentry.FormState.SAVING;

      var fields = void 0;
      var onSubmit = void 0;
      var submitLabel = void 0;
      if (this.state.editing) {
        fields = this.state.fieldList.filter(function (f) {
          return _this4.PAGE_FIELD_LIST[_this4.state.page].includes(f.name);
        });
        onSubmit = this.onSubmit;
        submitLabel = this.isLastPage() ? 'Finish' : 'Save and Continue';
      } else {
        fields = this.state.fieldList.map(function (f) {
          return Object.assign({}, f, { readonly: true });
        });
        onSubmit = this.startEditing;
        submitLabel = 'Edit';
      }
      return _react2.default.createElement(
        _sentry.Form,
        { onSubmit: onSubmit,
          submitDisabled: isSaving,
          submitLabel: submitLabel,
          extraButton: this.state.page === 0 ? null : _react2.default.createElement(
            'a',
            { href: '#',
              className: 'btn btn-default pull-left' + (isSaving ? ' disabled' : ''),
              onClick: this.back },
            'Back'
          ) },
        this.state.errors.__all__ && _react2.default.createElement(
          'div',
          { className: 'alert alert-block alert-error' },
          _react2.default.createElement(
            'ul',
            null,
            _react2.default.createElement(
              'li',
              null,
              this.state.errors.__all__
            )
          )
        ),
        fields.map(function (f) {
          return _this4.renderField({
            config: f,
            formData: _this4.state.formData,
            formErrors: _this4.state.errors,
            onChange: _this4.changeField.bind(_this4, f.name)
          });
        })
      );
    }
  }]);

  return Settings;
}(_sentry.plugins.BasePlugin.DefaultSettings);

exports.default = Settings;
module.exports = exports['default'];

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = __webpack_require__(0);

var _react2 = _interopRequireDefault(_react);

var _sentry = __webpack_require__(1);

var _settings = __webpack_require__(3);

var _settings2 = _interopRequireDefault(_settings);

var _issueActions = __webpack_require__(2);

var _issueActions2 = _interopRequireDefault(_issueActions);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Jira = function (_plugins$DefaultIssue) {
    _inherits(Jira, _plugins$DefaultIssue);

    function Jira() {
        _classCallCheck(this, Jira);

        return _possibleConstructorReturn(this, (Jira.__proto__ || Object.getPrototypeOf(Jira)).apply(this, arguments));
    }

    _createClass(Jira, [{
        key: 'renderSettings',
        value: function renderSettings(props) {
            return _react2.default.createElement(_settings2.default, _extends({ plugin: this }, props));
        }
    }, {
        key: 'renderGroupActions',
        value: function renderGroupActions(props) {
            return _react2.default.createElement(_issueActions2.default, _extends({ plugin: this }, props));
        }
    }]);

    return Jira;
}(_sentry.plugins.DefaultIssuePlugin);

Jira.displayName = 'Jira';

_sentry.plugins.add('jira', Jira);

exports.default = Jira;
module.exports = exports['default'];

/***/ }),
/* 5 */
/***/ (function(module, exports) {

module.exports = underscore;

/***/ })
/******/ ]);
//# sourceMappingURL=jira.js.map