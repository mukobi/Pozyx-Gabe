package com.psupozyx.app;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.ChoiceBox;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.IOException;

public class ConfigureUwbSettings {

    @FXML
    private ChoiceBox<String> m_channel;
    @FXML
    private ChoiceBox<String> m_bitrate;
    @FXML
    private ChoiceBox<String> m_prf;
    @FXML
    private ChoiceBox<String> m_plen;
    @FXML
    private ChoiceBox<String> m_gain;


    public void handleLaunchConfigureUwb() {
        String channel = m_channel.getValue();

        String unparsedBitrate = m_bitrate.getValue();
        String bitrate;
        switch (unparsedBitrate) {
            case "110 Mbps":
                bitrate = "0";
                break;
            case "850 Mbps":
                bitrate = "1";
                break;
            case "6810 Mbps":
                bitrate = "2";
                break;
            default:
                bitrate = "1";
                break;
        }

        String unparsedPrf = m_prf.getValue();
        String prf;
        switch (unparsedPrf) {
            case "16 MHz":
                prf = "1";
                break;
            case "64 MHz":
                prf = "2";
                break;
            default:
                prf = "2";
                break;
        }

        String unparsedPlen = m_plen.getValue();
        String plen;
        switch (unparsedPlen) {
            case "64":
                plen = "0x04";
                break;
            case "128":
                plen = "0x14";
                break;
            case "256":
                plen = "0x24";
                break;
            case "512":
                plen = "0x34";
                break;
            case "1024":
                plen = "0x08";
                break;
            case "1536":
                plen = "0x18";
                break;
            case "2048":
                plen = "0x28";
                break;
            case "4096":
                plen = "0x0C";
                break;
            default:
                plen = "0x08";
                break;
        }

        String gain = m_gain.getValue();

        String[] args =  {channel, bitrate, prf, plen, gain};

        new Controller().launchConsoleLogging("configure_uwb_settings", true, args, "PYINSTALLERPATH");
    }

    public void handleLaunchCheckUwb(ActionEvent actionEvent) {
        new Controller().launchConsoleLogging("configure_uwb_settings", true, null, "PYINSTALLERPATH");
    }

    public void handleMaximumRange() {
        m_bitrate.setValue("110 Mbps");
        m_plen.setValue("4096");
        m_gain.setValue("33.5");
    }

    public void handleFavorRange() {
        m_bitrate.setValue("110 Mbps");
        m_plen.setValue("2048");
        m_gain.setValue("25.0");
    }

    public void handleBalanced() {
        m_bitrate.setValue("850 Mbps");
        m_plen.setValue("1024");
        m_gain.setValue("15.0");
    }

    public void handleFavorDataRate() {
        m_bitrate.setValue("6810 Mbps");
        m_plen.setValue("256");
        m_gain.setValue("5.0");
    }

    public void handleMaximumDataRate() {
        m_bitrate.setValue("6810 Mbps");
        m_plen.setValue("64");
        m_gain.setValue("0.0");
    }

    public void handleQuit() {
        Platform.exit();
    }
}
