/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/_app";
exports.ids = ["pages/_app"];
exports.modules = {

/***/ "(pages-dir-node)/./contexts/ProjectContext.tsx":
/*!*************************************!*\
  !*** ./contexts/ProjectContext.tsx ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   ProjectProvider: () => (/* binding */ ProjectProvider),\n/* harmony export */   useProject: () => (/* binding */ useProject)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n\n\nconst ProjectContext = /*#__PURE__*/ (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)(undefined);\nfunction ProjectProvider({ children }) {\n    const [projects, setProjects] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)([]);\n    const [selectedProject, setSelectedProject] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(ProjectContext.Provider, {\n        value: {\n            projects,\n            setProjects,\n            selectedProject,\n            setSelectedProject\n        },\n        children: children\n    }, void 0, false, {\n        fileName: \"/home/runner/workspace/contexts/ProjectContext.tsx\",\n        lineNumber: 18,\n        columnNumber: 5\n    }, this);\n}\nfunction useProject() {\n    const context = (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(ProjectContext);\n    if (context === undefined) {\n        throw new Error('useProject must be used within a ProjectProvider');\n    }\n    return context;\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHBhZ2VzLWRpci1ub2RlKS8uL2NvbnRleHRzL1Byb2plY3RDb250ZXh0LnRzeCIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQXNFO0FBVXRFLE1BQU1HLCtCQUFpQkgsb0RBQWFBLENBQWlDSTtBQUU5RCxTQUFTQyxnQkFBZ0IsRUFBRUMsUUFBUSxFQUEyQjtJQUNuRSxNQUFNLENBQUNDLFVBQVVDLFlBQVksR0FBR04sK0NBQVFBLENBQVksRUFBRTtJQUN0RCxNQUFNLENBQUNPLGlCQUFpQkMsbUJBQW1CLEdBQUdSLCtDQUFRQSxDQUFpQjtJQUV2RSxxQkFDRSw4REFBQ0MsZUFBZVEsUUFBUTtRQUFDQyxPQUFPO1lBQzlCTDtZQUNBQztZQUNBQztZQUNBQztRQUNGO2tCQUNHSjs7Ozs7O0FBR1A7QUFFTyxTQUFTTztJQUNkLE1BQU1DLFVBQVViLGlEQUFVQSxDQUFDRTtJQUMzQixJQUFJVyxZQUFZVixXQUFXO1FBQ3pCLE1BQU0sSUFBSVcsTUFBTTtJQUNsQjtJQUNBLE9BQU9EO0FBQ1QiLCJzb3VyY2VzIjpbIi9ob21lL3J1bm5lci93b3Jrc3BhY2UvY29udGV4dHMvUHJvamVjdENvbnRleHQudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IGNyZWF0ZUNvbnRleHQsIHVzZUNvbnRleHQsIHVzZVN0YXRlLCBSZWFjdE5vZGUgfSBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFByb2plY3QgfSBmcm9tICdAL3R5cGVzJ1xuXG5pbnRlcmZhY2UgUHJvamVjdENvbnRleHRUeXBlIHtcbiAgcHJvamVjdHM6IFByb2plY3RbXVxuICBzZXRQcm9qZWN0czogKHByb2plY3RzOiBQcm9qZWN0W10gfCAoKHByZXY6IFByb2plY3RbXSkgPT4gUHJvamVjdFtdKSkgPT4gdm9pZFxuICBzZWxlY3RlZFByb2plY3Q6IFByb2plY3QgfCBudWxsXG4gIHNldFNlbGVjdGVkUHJvamVjdDogKHByb2plY3Q6IFByb2plY3QgfCBudWxsKSA9PiB2b2lkXG59XG5cbmNvbnN0IFByb2plY3RDb250ZXh0ID0gY3JlYXRlQ29udGV4dDxQcm9qZWN0Q29udGV4dFR5cGUgfCB1bmRlZmluZWQ+KHVuZGVmaW5lZClcblxuZXhwb3J0IGZ1bmN0aW9uIFByb2plY3RQcm92aWRlcih7IGNoaWxkcmVuIH06IHsgY2hpbGRyZW46IFJlYWN0Tm9kZSB9KSB7XG4gIGNvbnN0IFtwcm9qZWN0cywgc2V0UHJvamVjdHNdID0gdXNlU3RhdGU8UHJvamVjdFtdPihbXSlcbiAgY29uc3QgW3NlbGVjdGVkUHJvamVjdCwgc2V0U2VsZWN0ZWRQcm9qZWN0XSA9IHVzZVN0YXRlPFByb2plY3QgfCBudWxsPihudWxsKVxuXG4gIHJldHVybiAoXG4gICAgPFByb2plY3RDb250ZXh0LlByb3ZpZGVyIHZhbHVlPXt7XG4gICAgICBwcm9qZWN0cyxcbiAgICAgIHNldFByb2plY3RzLFxuICAgICAgc2VsZWN0ZWRQcm9qZWN0LFxuICAgICAgc2V0U2VsZWN0ZWRQcm9qZWN0XG4gICAgfX0+XG4gICAgICB7Y2hpbGRyZW59XG4gICAgPC9Qcm9qZWN0Q29udGV4dC5Qcm92aWRlcj5cbiAgKVxufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlUHJvamVjdCgpIHtcbiAgY29uc3QgY29udGV4dCA9IHVzZUNvbnRleHQoUHJvamVjdENvbnRleHQpXG4gIGlmIChjb250ZXh0ID09PSB1bmRlZmluZWQpIHtcbiAgICB0aHJvdyBuZXcgRXJyb3IoJ3VzZVByb2plY3QgbXVzdCBiZSB1c2VkIHdpdGhpbiBhIFByb2plY3RQcm92aWRlcicpXG4gIH1cbiAgcmV0dXJuIGNvbnRleHRcbn0iXSwibmFtZXMiOlsiY3JlYXRlQ29udGV4dCIsInVzZUNvbnRleHQiLCJ1c2VTdGF0ZSIsIlByb2plY3RDb250ZXh0IiwidW5kZWZpbmVkIiwiUHJvamVjdFByb3ZpZGVyIiwiY2hpbGRyZW4iLCJwcm9qZWN0cyIsInNldFByb2plY3RzIiwic2VsZWN0ZWRQcm9qZWN0Iiwic2V0U2VsZWN0ZWRQcm9qZWN0IiwiUHJvdmlkZXIiLCJ2YWx1ZSIsInVzZVByb2plY3QiLCJjb250ZXh0IiwiRXJyb3IiXSwiaWdub3JlTGlzdCI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(pages-dir-node)/./contexts/ProjectContext.tsx\n");

/***/ }),

/***/ "(pages-dir-node)/./pages/_app.tsx":
/*!************************!*\
  !*** ./pages/_app.tsx ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ App)\n/* harmony export */ });\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"react/jsx-dev-runtime\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/styles/globals.css */ \"(pages-dir-node)/./styles/globals.css\");\n/* harmony import */ var _styles_globals_css__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_styles_globals_css__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ \"react\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _contexts_ProjectContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @/contexts/ProjectContext */ \"(pages-dir-node)/./contexts/ProjectContext.tsx\");\n\n\n\n\nfunction App({ Component, pageProps }) {\n    const [mounted, setMounted] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(false);\n    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)({\n        \"App.useEffect\": ()=>{\n            setMounted(true);\n        }\n    }[\"App.useEffect\"], []);\n    if (!mounted) {\n        return null;\n    }\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_contexts_ProjectContext__WEBPACK_IMPORTED_MODULE_3__.ProjectProvider, {\n        children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(Component, {\n            ...pageProps\n        }, void 0, false, {\n            fileName: \"/home/runner/workspace/pages/_app.tsx\",\n            lineNumber: 19,\n            columnNumber: 7\n        }, this)\n    }, void 0, false, {\n        fileName: \"/home/runner/workspace/pages/_app.tsx\",\n        lineNumber: 18,\n        columnNumber: 5\n    }, this);\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHBhZ2VzLWRpci1ub2RlKS8uL3BhZ2VzL19hcHAudHN4IiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7OztBQUE2QjtBQUVjO0FBQ2dCO0FBRTVDLFNBQVNHLElBQUksRUFBRUMsU0FBUyxFQUFFQyxTQUFTLEVBQVk7SUFDNUQsTUFBTSxDQUFDQyxTQUFTQyxXQUFXLEdBQUdQLCtDQUFRQSxDQUFDO0lBRXZDQyxnREFBU0E7eUJBQUM7WUFDUk0sV0FBVztRQUNiO3dCQUFHLEVBQUU7SUFFTCxJQUFJLENBQUNELFNBQVM7UUFDWixPQUFPO0lBQ1Q7SUFFQSxxQkFDRSw4REFBQ0oscUVBQWVBO2tCQUNkLDRFQUFDRTtZQUFXLEdBQUdDLFNBQVM7Ozs7Ozs7Ozs7O0FBRzlCIiwic291cmNlcyI6WyIvaG9tZS9ydW5uZXIvd29ya3NwYWNlL3BhZ2VzL19hcHAudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAnQC9zdHlsZXMvZ2xvYmFscy5jc3MnXG5pbXBvcnQgdHlwZSB7IEFwcFByb3BzIH0gZnJvbSAnbmV4dC9hcHAnXG5pbXBvcnQgeyB1c2VTdGF0ZSwgdXNlRWZmZWN0IH0gZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBQcm9qZWN0UHJvdmlkZXIgfSBmcm9tICdAL2NvbnRleHRzL1Byb2plY3RDb250ZXh0J1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBBcHAoeyBDb21wb25lbnQsIHBhZ2VQcm9wcyB9OiBBcHBQcm9wcykge1xuICBjb25zdCBbbW91bnRlZCwgc2V0TW91bnRlZF0gPSB1c2VTdGF0ZShmYWxzZSlcblxuICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgIHNldE1vdW50ZWQodHJ1ZSlcbiAgfSwgW10pXG5cbiAgaWYgKCFtb3VudGVkKSB7XG4gICAgcmV0dXJuIG51bGxcbiAgfVxuXG4gIHJldHVybiAoXG4gICAgPFByb2plY3RQcm92aWRlcj5cbiAgICAgIDxDb21wb25lbnQgey4uLnBhZ2VQcm9wc30gLz5cbiAgICA8L1Byb2plY3RQcm92aWRlcj5cbiAgKVxufSJdLCJuYW1lcyI6WyJ1c2VTdGF0ZSIsInVzZUVmZmVjdCIsIlByb2plY3RQcm92aWRlciIsIkFwcCIsIkNvbXBvbmVudCIsInBhZ2VQcm9wcyIsIm1vdW50ZWQiLCJzZXRNb3VudGVkIl0sImlnbm9yZUxpc3QiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///(pages-dir-node)/./pages/_app.tsx\n");

/***/ }),

/***/ "(pages-dir-node)/./styles/globals.css":
/*!****************************!*\
  !*** ./styles/globals.css ***!
  \****************************/
/***/ (() => {



/***/ }),

/***/ "react":
/*!************************!*\
  !*** external "react" ***!
  \************************/
/***/ ((module) => {

"use strict";
module.exports = require("react");

/***/ }),

/***/ "react/jsx-dev-runtime":
/*!****************************************!*\
  !*** external "react/jsx-dev-runtime" ***!
  \****************************************/
/***/ ((module) => {

"use strict";
module.exports = require("react/jsx-dev-runtime");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(pages-dir-node)/./pages/_app.tsx"));
module.exports = __webpack_exports__;

})();