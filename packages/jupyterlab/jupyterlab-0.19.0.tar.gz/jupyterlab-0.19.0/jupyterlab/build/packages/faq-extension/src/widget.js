// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var virtualdom_1 = require("@phosphor/virtualdom");
var apputils_1 = require("@jupyterlab/apputils");
/**
 * The class name added to the FAQ plugin.
 */
var FAQ_CLASS = 'jp-FAQ';
/**
 * The id name added to the header section element.
 */
var HEADER_ID = 'faq-header';
/**
 * The class name added to the title.
 */
var TITLE_CLASS = 'jp-FAQ-title';
/**
 * The class name added to h1 elements.
 */
var HEADER_CLASS = 'jp-FAQ-h1';
/**
 * The class name added to h2 elements.
 */
var SUBHEADER_CLASS = 'jp-FAQ-h2';
/**
 * The class name added for the question mark icon from default-theme.
 */
var QUESTIONMARK_ICON_CLASS = 'jp-QuestionMark';
/**
 * The class named added the question mark icon.
 */
var QUESTIONMARK_CLASS = 'jp-FAQ-QuestionMark';
/**
 * The class name added to faq content.
 */
var CONTENT_CLASS = 'jp-FAQ-content';
/**
 * The class name added to unordered list elements.
 */
var FAQ_LIST_CLASS = 'jp-FAQ-ul';
/**
 * The class name added to table of contents elements.
 */
var TOC_CLASS = 'jp-FAQ-toc';
/**
 * The class name added to questions.
 */
var QUESTION_CLASS = 'jp-FAQ-question';
/**
 * The class name added to answers.
 */
var ANSWER_CLASS = 'jp-FAQ-answer';
/**
 * The class name added to anchor elements.
 */
var ANCHOR_CLASS = 'jp-FAQ-a';
/**
 * Title of the FAQ plugin.
 */
var TITLE = 'Frequently Asked Questions';
/**
 * Contain subheadings for each section.
 */
var SUBHEADINGS = ['THE BASICS', 'FEATURES', 'DEVELOPER'];
/**
 * Contain questions for `the basics` section.
 */
var BASIC_QUESTIONS = [
    'What is JupyterLab?',
    'What is a Jupyter Notebook?',
    'How stable is JupyterLab?',
    "I'm confused with the interface. How do I navigate around JupyterLab?"
];
/**
 * Contain questions for the `features` section.
 */
var FEATURES_QUESTIONS = [
    'How do I add more kernels/languages to JupyterLab?',
    'How can I share my notebooks?'
];
/**
 * Contain questions for the `developer` section.
 */
var DEVELOPER_QUESTIONS = [
    'How do I report a bug?',
    'I have security concerns about JupyterLab.',
    'How can I contribute?'
];
/**
 * FaqModel holds data which the FaqWidget will render.
 */
var FaqModel = (function (_super) {
    __extends(FaqModel, _super);
    function FaqModel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Title of the FAQ plugin.
         */
        _this.title = TITLE;
        /**
         * Contain subheadings for each section.
         */
        _this.subheadings = SUBHEADINGS;
        /**
         * Contain questions for `the basics` section.
         */
        _this.basicsQuestions = BASIC_QUESTIONS;
        /**
         * Contain questions for the `features` section.
         */
        _this.featuresQuestions = FEATURES_QUESTIONS;
        /**
         * Contain questions for the `developer` section.
         */
        _this.developerQuestions = DEVELOPER_QUESTIONS;
        return _this;
    }
    return FaqModel;
}(apputils_1.VDomModel));
exports.FaqModel = FaqModel;
/**
 * A virtual-DOM-based widget for the FAQ plugin.
 */
var FaqWidget = (function (_super) {
    __extends(FaqWidget, _super);
    /**
     * Construct a new faq widget.
     */
    function FaqWidget(options) {
        var _this = _super.call(this) || this;
        _this._linker = options.linker;
        _this.addClass(FAQ_CLASS);
        return _this;
    }
    /**
     * Render the faq plugin to virtual DOM nodes.
     */
    FaqWidget.prototype.render = function () {
        var linker = this._linker;
        var subheadings = this.model.subheadings;
        var basicsQuestions = this.model.basicsQuestions;
        var featuresQuestions = this.model.featuresQuestions;
        var developerQuestions = this.model.developerQuestions;
        // Create Frequently Asked Questions Header Section.
        var faqHeader = virtualdom_1.h.section({ id: HEADER_ID }, virtualdom_1.h.span({
            className: QUESTIONMARK_ICON_CLASS + ' ' + QUESTIONMARK_CLASS
        }), virtualdom_1.h.h1({ className: HEADER_CLASS }, virtualdom_1.h.span({ className: TITLE_CLASS }, this.model.title)));
        // Create a section element that holds Table of Contents.
        var questionList = virtualdom_1.h.section({ className: CONTENT_CLASS }, virtualdom_1.h.h2({ className: SUBHEADER_CLASS }, subheadings[0]), virtualdom_1.h.ul({ className: FAQ_LIST_CLASS }, virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#basicsQ1' }, basicsQuestions[0])), virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#basicsQ2' }, basicsQuestions[1])), virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#basicsQ3' }, basicsQuestions[2])), virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#basicsQ4' }, basicsQuestions[3]))), virtualdom_1.h.h2({ className: SUBHEADER_CLASS }, subheadings[1]), virtualdom_1.h.ul({ className: FAQ_LIST_CLASS }, virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#featuresQ1' }, featuresQuestions[0])), virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#featuresQ2' }, featuresQuestions[1]))), virtualdom_1.h.h2({ className: SUBHEADER_CLASS }, subheadings[2]), virtualdom_1.h.ul({ className: FAQ_LIST_CLASS }, virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#developerQ1' }, developerQuestions[0])), virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#developerQ2' }, developerQuestions[1])), virtualdom_1.h.li({ className: QUESTION_CLASS + ' ' + TOC_CLASS }, virtualdom_1.h.a({ href: '#developerQ3' }, developerQuestions[2]))));
        // Create a section element that all other FAQ Content will go under.
        var questionAnswerList = virtualdom_1.h.section({ className: CONTENT_CLASS }, virtualdom_1.h.h2({ className: SUBHEADER_CLASS }, subheadings[0]), 
        // Create list of questions/answers under the Basics section.
        virtualdom_1.h.ul({ className: FAQ_LIST_CLASS }, virtualdom_1.h.li({ className: QUESTION_CLASS, id: 'basicsQ1' }, basicsQuestions[0]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "JupyterLab allows users to arrange multiple Jupyter notebooks,\n          text editors, terminals, output areas, etc. on a single page with\n          multiple panels and tabs into one application. The codebase and UI of\n          JupyterLab is based on a flexible plugin system that makes it easy to\n          extend with new components."), virtualdom_1.h.li({ className: QUESTION_CLASS, id: 'basicsQ2' }, basicsQuestions[1]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "Central to the project is the Jupyter Notebook, a web-based\n          platform that allows users to combine live code, equations, narrative\n          text, visualizations, interactive dashboards and other media. Together\n          these building blocks make science and data reproducible across over\n          40 programming languages and combine to form what we call a\n          computational narrative."), virtualdom_1.h.li({ className: QUESTION_CLASS, id: 'basicsQ3' }, basicsQuestions[2]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "JupyterLab is currently in an alpha release and not ready for public\n          use as new features and bug fixes are being added very frequently. We\n          strongly recommend to back up your work before using JupyterLab.\n          However, testing, development, and user feedback are greatly\n          appreciated."), virtualdom_1.h.li({ className: QUESTION_CLASS, id: 'basicsQ4' }, basicsQuestions[3]), virtualdom_1.h.li({ className: ANSWER_CLASS }, 'Check out the JupyterLab tour ', virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            dataset: linker.populateVNodeDataset('about-jupyterlab:open', null)
        }, 'here'))), virtualdom_1.h.h2({ className: SUBHEADER_CLASS }, subheadings[1]), 
        // Create list of questions/answers under the Features section.
        virtualdom_1.h.ul({ className: FAQ_LIST_CLASS }, virtualdom_1.h.li({
            className: QUESTION_CLASS,
            id: 'featuresQ1'
        }, featuresQuestions[0]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "To add more languages to the JupyterLab you must install a new\n          kernel. Installing a kernel is usually fairly simple and can be done\n          with a couple terminal commands. However the instructions for\n          installing kernels is different for each language. For further\n          instructions, click", virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'https://jupyter.readthedocs.io/en/latest/install-kernel.html',
            target: '_blank'
        }, 'this'), ' link.'), virtualdom_1.h.li({
            className: QUESTION_CLASS,
            id: 'featuresQ2'
        }, featuresQuestions[1]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "You can either publish your notebooks on GitHub or use a free service\n          such as ", virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'https://nbviewer.jupyter.org/',
            target: '_blank'
        }, 'nbviewer.org'), ' to render your notebooks online.')), virtualdom_1.h.h2({ className: SUBHEADER_CLASS }, subheadings[2]), 
        // Create list of questions/answers under the Developer section.
        virtualdom_1.h.ul({ className: FAQ_LIST_CLASS }, virtualdom_1.h.li({
            className: QUESTION_CLASS,
            id: 'developerQ1'
        }, developerQuestions[0]), virtualdom_1.h.li({ className: ANSWER_CLASS }, 'You can open an issue on our ', virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'https://github.com/jupyterlab/jupyterlab/issues',
            target: '_blank'
        }, 'GitHub repository'), '. Please check already opened issues before posting.'), virtualdom_1.h.li({
            className: QUESTION_CLASS,
            id: 'developerQ2'
        }, developerQuestions[1]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "If you have any inquiries, concerns, or thought you found a security\n          vulnerability, please write to use at ", virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'mailto:security@jupyter.org'
        }, 'security@jupyter.org'), '. We will do our best to repond to you promptly.'), virtualdom_1.h.li({
            className: QUESTION_CLASS,
            id: 'developerQ3'
        }, developerQuestions[2]), virtualdom_1.h.li({ className: ANSWER_CLASS }, "There are many ways to contribute to JupyterLab. Whether you are an\n          experienced Python programmer or a newcomer, any interested developers\n          are welcome. You can learn about the JupyterLab codebase by going\n          through our", virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'https://jupyterlab-tutorial.readthedocs.io/en/latest/index.html',
            target: '_blank'
        }, 'tutorial walkthrough'), ' and ', virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'https://jupyterlab.github.io/jupyterlab/',
            target: '_blank'
        }, 'documentation'), '. Also, feel free to ask questions on our ', virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'https://github.com/jupyterlab/jupyterlab',
            target: '_blank'
        }, 'github'), ' or through any of our ', virtualdom_1.h.a({
            className: ANCHOR_CLASS,
            href: 'http://jupyter.org/community.html',
            target: '_blank'
        }, 'community resources'), '.')));
        return [faqHeader, questionList, questionAnswerList];
    };
    /**
     * Handle `'activate-request'` messages.
     */
    FaqWidget.prototype.onActivateRequest = function (msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    };
    /**
     * Handle `'close-request'` messages.
     */
    FaqWidget.prototype.onCloseRequest = function (msg) {
        _super.prototype.onCloseRequest.call(this, msg);
        this.dispose();
    };
    return FaqWidget;
}(apputils_1.VDomWidget));
exports.FaqWidget = FaqWidget;
