'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.reduxBridge = exports.webSocketBridge = exports.WebSocketBridge = undefined;

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _reconnectingWebsocket = require('reconnecting-websocket');

var _reconnectingWebsocket2 = _interopRequireDefault(_reconnectingWebsocket);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var noop = function noop() {};

/**
 * Bridge between Channels and plain javascript.
 *
 * @example
 * const webSocketBridge = new WebSocketBridge();
 * webSocketBridge.connect();
 * webSocketBridge.listen(function(action, stream) {
 *   console.log(action, stream);
 * });
 */

var WebSocketBridge = function () {
  function WebSocketBridge(options) {
    _classCallCheck(this, WebSocketBridge);

    this._socket = null;
    this.streams = {};
    this.default_cb = null;
    this.options = Objec.assign({}, {
      onopen: noop
    }, options);
  }

  /**
   * Connect to the websocket server
   *
   * @param      {String}  [url]     The url of the websocket. Defaults to
   * `window.location.host`
   * @example
   * const webSocketBridge = new WebSocketBridge();
   * webSocketBridge.connect();
   */


  _createClass(WebSocketBridge, [{
    key: 'connect',
    value: function connect(url) {
      var _url = void 0;
      if (url === undefined) {
        // Use wss:// if running on https://
        var scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
        _url = scheme + '://' + window.location.host + '/ws';
      } else {
        _url = url;
      }
      this._socket = new _reconnectingWebsocket2.default(_url);
    }

    /**
     * Starts listening for messages on the websocket, demultiplexing if necessary.
     *
     * @param      {Function}  [cb]         Callback to be execute when a message
     * arrives. The callback will receive `action` and `stream` parameters
     *
     * @example
     * const webSocketBridge = new WebSocketBridge();
     * webSocketBridge.connect();
     * webSocketBridge.listen(function(action, stream) {
     *   console.log(action, stream);
     * });
     */

  }, {
    key: 'listen',
    value: function listen(cb) {
      var _this = this;

      this.default_cb = cb;
      this._socket.onmessage = function (event) {
        var msg = JSON.parse(event.data);
        var action = void 0;
        var stream = void 0;
        if (msg.stream !== undefined && _this.streams[msg.stream] !== undefined) {
          action = msg.payload;
          stream = msg.stream;
          var stream_cb = _this.streams[stream];
          stream_cb ? stream_cb(action, stream) : null;
        } else {
          action = msg;
          stream = null;
          _this.default_cb ? _this.default_cb(action, stream) : null;
        }
      };

      this._socket.onopen = this.options.onopen;
    }

    /**
     * Adds a 'stream handler' callback. Messages coming from the specified stream
     * will call the specified callback.
     *
     * @param      {String}    stream  The stream name
     * @param      {Function}  cb      Callback to be execute when a message
     * arrives. The callback will receive `action` and `stream` parameters.
      * @example
     * const webSocketBridge = new WebSocketBridge();
     * webSocketBridge.connect();
     * webSocketBridge.listen();
     * webSocketBridge.demultiplex('mystream', function(action, stream) {
     *   console.log(action, stream);
     * });
     * webSocketBridge.demultiplex('myotherstream', function(action, stream) {
     *   console.info(action, stream);
     * });
     */

  }, {
    key: 'demultiplex',
    value: function demultiplex(stream, cb) {
      this.streams[stream] = cb;
    }

    /**
     * Sends a message to the reply channel.
     *
     * @param      {Object}  msg     The message
     *
     * @example
     * // We cheat by using the Redux-style Actions as our
     * // communication protocol with the server. Consider separating
     * // communication format from client-side action API.
     * webSocketBridge.send({type: 'MYACTION', 'payload': 'somepayload'});
     */

  }, {
    key: 'send',
    value: function send(msg) {
      this._socket.send(JSON.stringify(msg));
    }

    /**
     * Returns an object to send messages to a specific stream
     *
     * @param      {String}  stream  The stream name
     * @return     {Object}  convenience object to send messages to `stream`.
     * @example
     * // We cheat by using the Redux-style Actions as our
     * // communication protocol with the server. Consider separating
     * // communication format from client-side action API.
     * webSocketBridge.stream('mystream').send({type: 'MYACTION', 'payload': 'somepayload'})
     */

  }, {
    key: 'stream',
    value: function stream(_stream) {
      var _this2 = this;

      return {
        send: function send(action) {
          var msg = {
            stream: _stream,
            payload: action
          };
          _this2._socket.send(JSON.stringify(msg));
        }
      };
    }
  }]);

  return WebSocketBridge;
}();

/**
 * Convenience singleton for `WebSocketBridge`.
 * @example
 * import { webSocketBridge } from 'django_redux';
 *
 * webSocketBridge.connect();
 * webSocketBridge.listen(function(action, stream) { console.log(action) });
 *
 * @type       {WebSocketBridge}
 */


exports.WebSocketBridge = WebSocketBridge;
var webSocketBridge = exports.webSocketBridge = new WebSocketBridge();

/**
 * Bridge between Channels and Redux.
 * By default dispatches actions received from channels to the redux store.
 *
 * @example
 * const reduxBridge = new ReduxBridge();
 * reduxBridge.connect();
 * reduxBridge.listen(store);
 */

var ReduxBridge = function (_WebSocketBridge) {
  _inherits(ReduxBridge, _WebSocketBridge);

  function ReduxBridge(options) {
    _classCallCheck(this, ReduxBridge);

    options = _extends({}, {
      onreconnect: noop
    }, options);
    return _possibleConstructorReturn(this, (ReduxBridge.__proto__ || Object.getPrototypeOf(ReduxBridge)).call(this, options));
  }

  _createClass(ReduxBridge, [{
    key: 'listen',
    value: function listen(store) {
      var _this4 = this;

      var cb = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : this.storeDispatch;

      this.default_cb = cb;
      this._socket.onmessage = function (event) {
        var msg = JSON.parse(event.data);
        var action = void 0;
        var stream = void 0;
        if (msg.stream !== undefined && _this4.streams[msg.stream] !== undefined) {
          action = msg.payload;
          stream = msg.stream;
          var stream_cb = _this4.streams[stream];
          stream_cb(store, action, stream);
        } else {
          action = msg;
          stream = null;
          _this4.default_cb(store, action, stream);
        }
      };

      this._socket.onopen = function () {
        var state = store.getState();

        if (state.currentUser !== null) {
          // the connection was dropped. Call the recovery logic
          _this4.options.onreconnect(state);
        }
      };
    }
  }, {
    key: 'storeDispatch',
    value: function storeDispatch(store, action, stream) {
      return store.dispatch(action);
    }
  }]);

  return ReduxBridge;
}(WebSocketBridge);

/**
 * Convenience singleton for `ReduxSocketBridge`.
 * @example
 * import { ReduxBridge } from 'django_redux';
 *
 * ReduxBridge.connect();
 * ReduxBridge.listen(store);
 *
 * @type       {ReduxSocketBridge}
 */


var reduxBridge = exports.reduxBridge = new ReduxBridge();