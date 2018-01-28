package com.psupozyx.app;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ChoiceBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.*;
import java.net.URISyntaxException;
import java.util.Objects;

public class DataReplay {
    private Stage stage = (Stage) null;

    @FXML
    private CheckBox m_show_console_output;
    @FXML
    private CheckBox m_show_graphical_output;
    @FXML
    private ChoiceBox<String> m_speed;

    @FXML
    private CheckBox m_log_pressure;
    @FXML
    private CheckBox m_log_acceleration;
    @FXML
    private CheckBox m_log_magnetic;
    @FXML
    private CheckBox m_log_angular_velocity;
    @FXML
    private CheckBox m_log_euler_angles;
    @FXML
    private CheckBox m_log_quaternion;
    @FXML
    private CheckBox m_log_linear_acceleration;
    @FXML
    private CheckBox m_log_gravity;

    public void handleOpenReplayFile() {
        FileChooser fileChooser = new FileChooser();
        configureFileChooser(fileChooser);
        File loadFile = fileChooser.showOpenDialog(stage);
        String replayFileName = null;
        if (loadFile != null) {
            replayFileName = loadFile.getAbsolutePath();
            boolean show_console_output = m_show_console_output.isSelected();

            boolean show_graphical_output = m_show_graphical_output.isSelected();

            String replaySpeed;

            String gui_replay_speed = m_speed.getValue();

            if(Objects.equals(gui_replay_speed, "As fast as possible")) {
                replaySpeed = "0";
            }
            else {
                replaySpeed = gui_replay_speed.substring(0, gui_replay_speed.indexOf('x'));
            }

            String attributesToLog = "";

            if(m_log_pressure.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_acceleration.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_magnetic.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_angular_velocity.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_euler_angles.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_quaternion.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_linear_acceleration.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }
            if(m_log_gravity.isSelected()) { attributesToLog += '1'; }
            else { attributesToLog += '0'; }


            String pythonCommands = "python -u DataReplay/data_replay.py"
                    + " " + replayFileName + " " + replaySpeed + " " + attributesToLog;

            if(show_graphical_output) {
                try {
                    BufferedReader reader = new BufferedReader(new FileReader(replayFileName));
                    String headerLine = reader.readLine();
                    reader.close();
                    if(headerLine.contains("Pressure")) {
                        launchMotionProcessing();
                    }
                    else {
                        launchPositionProcessing();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            launchConsoleLogging(pythonCommands, show_console_output);
        }
    }

    private void launchMotionProcessing() {
        try {
            File this_file = new File(
                    Main.class.getProtectionDomain().getCodeSource().getLocation().toURI().getPath());
            File house_dir = this_file.getParentFile().getParentFile();
            if(house_dir.toString().endsWith("main_programs")) {
                house_dir = house_dir.getParentFile();
            }
            File parent = new File(house_dir.toString() +
                    "\\processing\\pozyx_orientation3D_PSU\\application.windows64\\");
            String executable = parent.toString() + "\\pozyx_orientation3D_PSU.exe";
            Runtime.getRuntime().exec(executable, null, parent);
        } catch (URISyntaxException | IOException e) {
            e.printStackTrace();
        }
    }

    private void launchPositionProcessing() {
        try {
            File this_file = new File(
                    Main.class.getProtectionDomain().getCodeSource().getLocation().toURI().getPath());
            File house_dir = this_file.getParentFile().getParentFile();
            if(house_dir.toString().endsWith("main_programs")) {
                house_dir = house_dir.getParentFile();
            }
            File parent = new File(house_dir.toString() +
                    "\\processing\\pozyx_ready_to_localize_PSU\\application.windows64\\");
            String executable = parent.toString() + "\\pozyx_ready_to_localize_PSU.exe";
            Runtime.getRuntime().exec(executable, null, parent);
        } catch (URISyntaxException | IOException e) {
            e.printStackTrace();
        }
    }




    public void handleQuit() {
        Platform.exit();
    }

    private void launchConsoleLogging(String pythonCommands, boolean showConsole) {
        try {
            Stage stage = new Stage();
            FXMLLoader loader = new FXMLLoader(getClass().getResource("fxml/console_window.fxml"));
            Parent root1 = loader.load();
            stage.setTitle("Data Replayer Console Output");
            stage.setScene(new Scene(root1));
            stage.setMaximized(false);
            stage.initOwner(m_speed.getScene().getWindow());
            stage.initStyle(StageStyle.DECORATED);
            ConsoleWindow console_controller = loader.getController();
            stage.setOnCloseRequest(we -> console_controller.terminateProcess());
            if (showConsole) {
                stage.show();
            }
            String prependPathType = "";
            console_controller.launchScript("", pythonCommands, null, prependPathType);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void configureFileChooser(final FileChooser fileChooser) {
        fileChooser.setTitle("Choose file to replay");
        fileChooser.getExtensionFilters().add(
                new FileChooser.ExtensionFilter("Comma Separated Values", "*.csv")
        );
    }

    public void handleConfigureUwbSettings(ActionEvent actionEvent) {
        Main main = new Main();
        main.openStage("/psupozyx/fxml/configure_uwb_settings.fxml", "PSU Pozyx | UWB Settings", 1024, 768);
    }
}
