/********************************************************************************
** Form generated from reading ui file 'about.ui'
**
** Created: Tue Aug 18 18:36:39 2009
**      by: Qt User Interface Compiler version 4.5.2
**
** WARNING! All changes made in this file will be lost when recompiling ui file!
********************************************************************************/

#ifndef UI_ABOUT_H
#define UI_ABOUT_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QDialog>
#include <QtGui/QGridLayout>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QPushButton>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_about_window
{
public:
    QGridLayout *gridLayout;
    QWidget *widget;
    QGridLayout *gridLayout1;
    QWidget *widget_2;
    QLabel *label_10;
    QLabel *label_2;
    QLabel *label;
    QLabel *label_6;
    QLabel *label_8;
    QLabel *label_9;
    QLabel *mucLink;
    QLabel *label_12;
    QLabel *version;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_13;
    QLabel *label_3;
    QPushButton *pushButton;

    void setupUi(QDialog *about_window)
    {
        if (about_window->objectName().isEmpty())
            about_window->setObjectName(QString::fromUtf8("about_window"));
        about_window->resize(519, 326);
        QIcon icon;
        icon.addFile(QString::fromUtf8("images/16x16/apps/jabbim.png"), QSize(), QIcon::Normal, QIcon::Off);
        about_window->setWindowIcon(icon);
        gridLayout = new QGridLayout(about_window);
#ifndef Q_OS_MAC
        gridLayout->setSpacing(6);
#endif
#ifndef Q_OS_MAC
        gridLayout->setMargin(9);
#endif
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        widget = new QWidget(about_window);
        widget->setObjectName(QString::fromUtf8("widget"));
        gridLayout1 = new QGridLayout(widget);
        gridLayout1->setSpacing(0);
        gridLayout1->setMargin(0);
        gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
        widget_2 = new QWidget(widget);
        widget_2->setObjectName(QString::fromUtf8("widget_2"));
        label_10 = new QLabel(widget_2);
        label_10->setObjectName(QString::fromUtf8("label_10"));
        label_10->setGeometry(QRect(340, 190, 80, 32));
        label_10->setAlignment(Qt::AlignCenter);
        label_2 = new QLabel(widget_2);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(90, 80, 80, 32));
        label_2->setAlignment(Qt::AlignCenter);
        label = new QLabel(widget_2);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(90, 0, 80, 32));
        label->setTextFormat(Qt::RichText);
        label->setAlignment(Qt::AlignHCenter|Qt::AlignTop);
        label->setOpenExternalLinks(true);
        label_6 = new QLabel(widget_2);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(290, 90, 188, 105));
        label_6->setAlignment(Qt::AlignCenter);
        label_8 = new QLabel(widget_2);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        label_8->setGeometry(QRect(70, 110, 107, 30));
        label_8->setAlignment(Qt::AlignCenter);
        label_9 = new QLabel(widget_2);
        label_9->setObjectName(QString::fromUtf8("label_9"));
        label_9->setGeometry(QRect(70, 140, 129, 31));
        label_9->setAlignment(Qt::AlignCenter);
        mucLink = new QLabel(widget_2);
        mucLink->setObjectName(QString::fromUtf8("mucLink"));
        mucLink->setGeometry(QRect(40, 160, 194, 41));
        mucLink->setAlignment(Qt::AlignCenter);
        mucLink->setOpenExternalLinks(false);
        label_12 = new QLabel(widget_2);
        label_12->setObjectName(QString::fromUtf8("label_12"));
        label_12->setGeometry(QRect(50, 190, 171, 16));
        label_12->setAlignment(Qt::AlignCenter);
        label_12->setOpenExternalLinks(true);
        version = new QLabel(widget_2);
        version->setObjectName(QString::fromUtf8("version"));
        version->setGeometry(QRect(100, 30, 61, 16));
        version->setAlignment(Qt::AlignCenter);
        label_4 = new QLabel(widget_2);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(300, 30, 171, 30));
        label_4->setAlignment(Qt::AlignCenter);
        label_5 = new QLabel(widget_2);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(320, 60, 131, 32));
        label_5->setAlignment(Qt::AlignCenter);
        label_13 = new QLabel(widget_2);
        label_13->setObjectName(QString::fromUtf8("label_13"));
        label_13->setGeometry(QRect(280, 220, 209, 16));
        label_13->setAlignment(Qt::AlignCenter);
        label_3 = new QLabel(widget_2);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(330, 0, 117, 32));
        label_3->setAlignment(Qt::AlignCenter);
        pushButton = new QPushButton(widget_2);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(190, 270, 101, 27));
        pushButton->setLayoutDirection(Qt::LeftToRight);
        pushButton->setAutoDefault(false);
        pushButton->setDefault(true);
        pushButton->setFlat(false);

        gridLayout1->addWidget(widget_2, 0, 0, 1, 1);


        gridLayout->addWidget(widget, 0, 0, 1, 1);


        retranslateUi(about_window);
        QObject::connect(pushButton, SIGNAL(clicked()), about_window, SLOT(accept()));

        QMetaObject::connectSlotsByName(about_window);
    } // setupUi

    void retranslateUi(QDialog *about_window)
    {
        about_window->setWindowTitle(QApplication::translate("about_window", "About Jabbim", 0, QApplication::UnicodeUTF8));
        label_10->setText(QApplication::translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
" 	p, li { white-space: pre-wrap; }\n"
" 	</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
" 	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Thanks to:</span></p></body></html>", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
" 	p, li { white-space: pre-wrap; }\n"
" 	</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
" 	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">License:</span> </p></body></html>", 0, QApplication::UnicodeUTF8));
        label->setText(QApplication::translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
" 	p, li { white-space: pre-wrap; }\n"
" 	</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
" 	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Version:</span></p></body></html>", 0, QApplication::UnicodeUTF8));
        label_6->setText(QApplication::translate("about_window", "Josef 'Cornelius' Vyb\303\255\302\255ral\n"
"Josef 'Pepeq' Hal\303\255\304\215ek\n"
"J\303\241chym 'Kamahl' Barv\303\255nek\n"
"Michal 'Michich' Schmidt\n"
"Jan 'Pinky' Pinkas\n"
"Zenon 'Zenek' Kuder\n"
"and many translators and patchers", 0, QApplication::UnicodeUTF8));
        label_8->setText(QApplication::translate("about_window", "GNU GPL version 2\n"
" 	", 0, QApplication::UnicodeUTF8));
        label_9->setText(QApplication::translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
" 	p, li { white-space: pre-wrap; }\n"
" 	</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
" 	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Where you find us:</span></p></body></html>", 0, QApplication::UnicodeUTF8));
        mucLink->setText(QApplication::translate("about_window", "Conference: <a href='xmpp:jabbim@conf.netlab.cz?join'>jabbim@conf.netlab.cz</a>", 0, QApplication::UnicodeUTF8));
        label_12->setText(QApplication::translate("about_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Web: <a href=\"http://dev.jabbim.cz/jabbim\"><span style=\" text-decoration: underline; color:#0000ff;\">http://dev.jabbim.cz/jabbim</span></a></p></body></html>", 0, QApplication::UnicodeUTF8));
        version->setText(QApplication::translate("about_window", "$VERSION", 0, QApplication::UnicodeUTF8));
        label_4->setText(QApplication::translate("about_window", "Jan 'HanzZ' Kalu\305\276a\n"
" 	Ji\305\231\303\255\302\255 'Sef' Gabry\305\241", 0, QApplication::UnicodeUTF8));
        label_5->setText(QApplication::translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
" 	p, li { white-space: pre-wrap; }\n"
" 	</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
" 	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Other developers:</span></p></body></html>", 0, QApplication::UnicodeUTF8));
        label_13->setText(QApplication::translate("about_window", "We thank all testers and bug reporters!", 0, QApplication::UnicodeUTF8));
        label_3->setText(QApplication::translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
" 	p, li { white-space: pre-wrap; }\n"
" 	</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
" 	<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Main developers:</span></p></body></html>", 0, QApplication::UnicodeUTF8));
        pushButton->setText(QApplication::translate("about_window", "OK", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(about_window);
    } // retranslateUi

};

namespace Ui {
    class about_window: public Ui_about_window {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ABOUT_H
