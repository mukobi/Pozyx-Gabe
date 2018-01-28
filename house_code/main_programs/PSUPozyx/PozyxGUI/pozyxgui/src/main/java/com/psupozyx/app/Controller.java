package com.psupozyx.app;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.stage.*;

import javax.swing.filechooser.FileSystemView;
import java.io.*;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Objects;
import java.util.Properties;
import java.util.ResourceBundle;

import static java.lang.String.valueOf;


public class Controller implements Initializable {
    private Stage stage = (Stage) null;

    // interface fields
    @FXML
    private ChoiceBox<String> m_number_mobile_devices;

    @FXML
    private TextField m_mobile_device_1_id;
    @FXML
    private TextField m_mobile_device_2_id;
    @FXML
    private TextField m_mobile_device_3_id;
    @FXML
    private TextField m_mobile_device_4_id;
    @FXML
    private TextField m_mobile_device_5_id;
    @FXML
    private TextField m_mobile_device_6_id;

    @FXML
    private TextField m_range_anchor_id;
    @FXML
    private CheckBox m_use_remote_1d_anchor;

    @FXML
    private ChoiceBox<String> m_number_anchors;

    @FXML
    private TextField m_a1_id;
    @FXML
    private TextField m_a1_x;
    @FXML
    private TextField m_a1_y;
    @FXML
    private TextField m_a1_z;
    @FXML
    private TextField m_a2_id;
    @FXML
    private TextField m_a2_x;
    @FXML
    private TextField m_a2_y;
    @FXML
    private TextField m_a2_z;
    @FXML
    private TextField m_a3_id;
    @FXML
    private TextField m_a3_x;
    @FXML
    private TextField m_a3_y;
    @FXML
    private TextField m_a3_z;
    @FXML
    private TextField m_a4_id;
    @FXML
    private TextField m_a4_x;
    @FXML
    private TextField m_a4_y;
    @FXML
    private TextField m_a4_z;
    @FXML
    private TextField m_a5_id;
    @FXML
    private TextField m_a5_x;
    @FXML
    private TextField m_a5_y;
    @FXML
    private TextField m_a5_z;
    @FXML
    private TextField m_a6_id;
    @FXML
    private TextField m_a6_x;
    @FXML
    private TextField m_a6_y;
    @FXML
    private TextField m_a6_z;
    @FXML
    private TextField m_a7_id;
    @FXML
    private TextField m_a7_x;
    @FXML
    private TextField m_a7_y;
    @FXML
    private TextField m_a7_z;
    @FXML
    private TextField m_a8_id;
    @FXML
    private TextField m_a8_x;
    @FXML
    private TextField m_a8_y;
    @FXML
    private TextField m_a8_z;

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

    @FXML
    private Spinner<Integer> m_position_smooth;
    @FXML
    private Spinner<Integer> m_velocity_smooth;

    @FXML
    private CheckBox m_use_file;
    @FXML
    private TextField m_filename;

    // field data variables
    private String number_mobile_devices;
    private String remote_1_id;
    private String remote_2_id;
    private String remote_3_id;
    private String remote_4_id;
    private String remote_5_id;
    private String remote_6_id;

    private String range_anchor_id;
    private String use_remote_1d_anchor;

    private String number_anchors;
    private String anchor1_id;
    private String anchor1_x;
    private String anchor1_y;
    private String anchor1_z;
    private String anchor2_id;
    private String anchor2_x;
    private String anchor2_y;
    private String anchor2_z;
    private String anchor3_id;
    private String anchor3_x;
    private String anchor3_y;
    private String anchor3_z;
    private String anchor4_id;
    private String anchor4_x;
    private String anchor4_y;
    private String anchor4_z;
    private String anchor5_id;
    private String anchor5_x;
    private String anchor5_y;
    private String anchor5_z;
    private String anchor6_id;
    private String anchor6_x;
    private String anchor6_y;
    private String anchor6_z;
    private String anchor7_id;
    private String anchor7_x;
    private String anchor7_y;
    private String anchor7_z;
    private String anchor8_id;
    private String anchor8_x;
    private String anchor8_y;
    private String anchor8_z;

    private String log_pressure;
    private String log_acceleration;
    private String log_magnetic;
    private String log_angular_velocity;
    private String log_euler_angles;
    private String log_quaternion;
    private String log_linear_acceleration;
    private String log_gravity;

    private String position_smooth;
    private String velocity_smooth;

    private String use_file;
    private String filename;


    @FXML
    private void handleLoadButtonAction() {
        update_variables_from_gui();
        FileChooser fileChooser = new FileChooser();
        configureFileChooser(fileChooser);
        File loadFile = fileChooser.showOpenDialog(stage);
        if (loadFile != null) {
            String templatePath = loadFile.getAbsolutePath();
            load_properties_from_file(templatePath);
        }
    }

    @FXML
    private void handleSaveTemplateButtonAction() {
        update_variables_from_gui();

        FileChooser fileChooser = new FileChooser();
        configureFileChooser(fileChooser);
        File templateFile = fileChooser.showSaveDialog(stage);
        if (templateFile != null) {
            String templatePath = templateFile.getAbsolutePath();
            save_properties_to_file(templatePath);
        }
    }

    private void saveSettingsForUse() {
        update_variables_from_gui();
        save_properties_to_file(GetDocumentsFolder() + "Configurations/MASTER_ACTIVE_CONFIG.properties");
    }

    @FXML
    private void handleLaunchRanging() {
        saveSettingsForUse();
        launchConsoleLogging("1D_ranging", true, null,"COMPILEDPATH");
    }
    @FXML
    private void handleLaunchPositioning() {
        saveSettingsForUse();
        launchConsoleLogging("3D_positioning", true, null, "COMPILEDPATH");
    }
    @FXML
    private void handleLaunchMotionData() {
        saveSettingsForUse();
        launchConsoleLogging("motion_data", true, null, "COMPILEDPATH");
    }
    @FXML
    private void handleLaunchPositioningAndMotionData() {
        saveSettingsForUse();
    }

    @FXML
    private void toggleAllSensorData() {
        update_variables_from_gui();
        if(Objects.equals(log_pressure, "true") &&
                Objects.equals(log_acceleration, "true") &&
                Objects.equals(log_magnetic, "true") &&
                Objects.equals(log_angular_velocity, "true") &&
                Objects.equals(log_euler_angles, "true") &&
                Objects.equals(log_quaternion, "true") &&
                Objects.equals(log_linear_acceleration, "true") &&
                Objects.equals(log_gravity, "true")) {
            m_log_pressure.setSelected(false);
            m_log_acceleration.setSelected(false);
            m_log_magnetic.setSelected(false);
            m_log_angular_velocity.setSelected(false);
            m_log_euler_angles.setSelected(false);
            m_log_quaternion.setSelected(false);
            m_log_linear_acceleration.setSelected(false);
            m_log_gravity.setSelected(false);
        }
        else {
            m_log_pressure.setSelected(true);
            m_log_acceleration.setSelected(true);
            m_log_magnetic.setSelected(true);
            m_log_angular_velocity.setSelected(true);
            m_log_euler_angles.setSelected(true);
            m_log_quaternion.setSelected(true);
            m_log_linear_acceleration.setSelected(true);
            m_log_gravity.setSelected(true);
        }
        update_variables_from_gui();
    }

    private void update_variables_from_gui() {
        number_mobile_devices = m_number_mobile_devices.getValue();
        remote_1_id = m_mobile_device_1_id.getText();
        remote_2_id = m_mobile_device_2_id.getText();
        remote_3_id = m_mobile_device_3_id.getText();
        remote_4_id = m_mobile_device_4_id.getText();
        remote_5_id = m_mobile_device_5_id.getText();
        remote_6_id = m_mobile_device_6_id.getText();

        range_anchor_id = m_range_anchor_id.getText();
        use_remote_1d_anchor = valueOf(m_use_remote_1d_anchor.isSelected());

        number_anchors = m_number_anchors.getValue();
        anchor1_id = m_a1_id.getText();
        anchor1_x = m_a1_x.getText();
        anchor1_y = m_a1_y.getText();
        anchor1_z = m_a1_z.getText();
        anchor2_id = m_a2_id.getText();
        anchor2_x = m_a2_x.getText();
        anchor2_y = m_a2_y.getText();
        anchor2_z = m_a2_z.getText();
        anchor3_id = m_a3_id.getText();
        anchor3_x = m_a3_x.getText();
        anchor3_y = m_a3_y.getText();
        anchor3_z = m_a3_z.getText();
        anchor4_id = m_a4_id.getText();
        anchor4_x = m_a4_x.getText();
        anchor4_y = m_a4_y.getText();
        anchor4_z = m_a4_z.getText();
        anchor5_id = m_a5_id.getText();
        anchor5_x = m_a5_x.getText();
        anchor5_y = m_a5_y.getText();
        anchor5_z = m_a5_z.getText();
        anchor6_id = m_a6_id.getText();
        anchor6_x = m_a6_x.getText();
        anchor6_y = m_a6_y.getText();
        anchor6_z = m_a6_z.getText();
        anchor7_id = m_a7_id.getText();
        anchor7_x = m_a7_x.getText();
        anchor7_y = m_a7_y.getText();
        anchor7_z = m_a7_z.getText();
        anchor8_id = m_a8_id.getText();
        anchor8_x = m_a8_x.getText();
        anchor8_y = m_a8_y.getText();
        anchor8_z = m_a8_z.getText();

        log_pressure = valueOf(m_log_pressure.isSelected());
        log_acceleration = valueOf(m_log_acceleration.isSelected());
        log_magnetic = valueOf(m_log_magnetic.isSelected());
        log_angular_velocity = valueOf(m_log_angular_velocity.isSelected());
        log_euler_angles = valueOf(m_log_euler_angles.isSelected());
        log_quaternion = valueOf(m_log_quaternion.isSelected());
        log_linear_acceleration = valueOf(m_log_linear_acceleration.isSelected());
        log_gravity = valueOf(m_log_gravity.isSelected());

        position_smooth = valueOf(m_position_smooth.getValue());
        velocity_smooth = valueOf(m_velocity_smooth.getValue());

        use_file = valueOf(m_use_file.isSelected());
        filename = m_filename.getText();
    }

    private void save_properties_to_file(String file) {
        Properties props = new Properties();
        OutputStream output = null;
        if(!file.endsWith(".properties")) {
            file += ".properties";
        }
        try {

            output = new FileOutputStream(file);

            // set the properties value
            props.setProperty("number_remotes", number_mobile_devices);
            props.setProperty("remote_1_id", remote_1_id);
            props.setProperty("remote_2_id", remote_2_id);
            props.setProperty("remote_3_id", remote_3_id);
            props.setProperty("remote_4_id", remote_4_id);
            props.setProperty("remote_5_id", remote_5_id);
            props.setProperty("remote_6_id", remote_6_id);

            props.setProperty("range_anchor_id", range_anchor_id);
            props.setProperty("use_remote_1d_anchor", use_remote_1d_anchor);

            props.setProperty("number_anchors", number_anchors);
            props.setProperty("anchor_1_id", anchor1_id);
            props.setProperty("anchor_1_x", anchor1_x);
            props.setProperty("anchor_1_y", anchor1_y);
            props.setProperty("anchor_1_z", anchor1_z);
            props.setProperty("anchor_2_id", anchor2_id);
            props.setProperty("anchor_2_x", anchor2_x);
            props.setProperty("anchor_2_y", anchor2_y);
            props.setProperty("anchor_2_z", anchor2_z);
            props.setProperty("anchor_3_id", anchor3_id);
            props.setProperty("anchor_3_x", anchor3_x);
            props.setProperty("anchor_3_y", anchor3_y);
            props.setProperty("anchor_3_z", anchor3_z);
            props.setProperty("anchor_4_id", anchor4_id);
            props.setProperty("anchor_4_x", anchor4_x);
            props.setProperty("anchor_4_y", anchor4_y);
            props.setProperty("anchor_4_z", anchor4_z);
            props.setProperty("anchor_5_id", anchor5_id);
            props.setProperty("anchor_5_x", anchor5_x);
            props.setProperty("anchor_5_y", anchor5_y);
            props.setProperty("anchor_5_z", anchor5_z);
            props.setProperty("anchor_6_id", anchor6_id);
            props.setProperty("anchor_6_x", anchor6_x);
            props.setProperty("anchor_6_y", anchor6_y);
            props.setProperty("anchor_6_z", anchor6_z);
            props.setProperty("anchor_7_id", anchor7_id);
            props.setProperty("anchor_7_x", anchor7_x);
            props.setProperty("anchor_7_y", anchor7_y);
            props.setProperty("anchor_7_z", anchor7_z);
            props.setProperty("anchor_8_id", anchor8_id);
            props.setProperty("anchor_8_x", anchor8_x);
            props.setProperty("anchor_8_y", anchor8_y);
            props.setProperty("anchor_8_z", anchor8_z);

            props.setProperty("log_pressure", log_pressure);
            props.setProperty("log_acceleration", log_acceleration);
            props.setProperty("log_magnetic", log_magnetic);
            props.setProperty("log_angular_velocity", log_angular_velocity);
            props.setProperty("log_euler_angles", log_euler_angles);
            props.setProperty("log_quaternion", log_quaternion);
            props.setProperty("log_linear_acceleration", log_linear_acceleration);
            props.setProperty("log_gravity", log_gravity);

            props.setProperty("position_smooth", position_smooth);
            props.setProperty("velocity_smooth", velocity_smooth);

            props.setProperty("use_file", use_file);
            props.setProperty("filename", filename);

            // save properties to project root folder
            props.store(output, null);

        } catch (IOException io) {
            io.printStackTrace();
        } finally {
            if (output != null) {
                try {
                    output.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private void load_properties_from_file(String loadPath) {
        if(!loadPath.endsWith(".properties")) {
            return;
        }
        Properties prop = new Properties();
        try {
            //load a properties file from class path, inside static method
            FileInputStream stream = new FileInputStream(loadPath);
            prop.load(stream);
            //get the property value and print it out
            m_number_mobile_devices.setValue(prop.getProperty("number_remotes", "0"));
            m_mobile_device_1_id.setText(prop.getProperty("remote_1_id", ""));
            m_mobile_device_2_id.setText(prop.getProperty("remote_2_id", ""));
            m_mobile_device_3_id.setText(prop.getProperty("remote_3_id", ""));
            m_mobile_device_4_id.setText(prop.getProperty("remote_4_id", ""));
            m_mobile_device_5_id.setText(prop.getProperty("remote_5_id", ""));
            m_mobile_device_6_id.setText(prop.getProperty("remote_6_id", ""));

            m_range_anchor_id.setText(prop.getProperty("range_anchor_id", ""));
            m_use_remote_1d_anchor.setSelected(Boolean.valueOf(prop.getProperty("use_remote_1d_anchor", "false")));

            m_number_anchors.setValue(prop.getProperty("number_anchors", "4"));
            m_a1_id.setText(prop.getProperty("anchor_1_id", ""));
            m_a1_x.setText (prop.getProperty("anchor_1_x", ""));
            m_a1_y.setText (prop.getProperty("anchor_1_y", ""));
            m_a1_z.setText (prop.getProperty("anchor_1_z", ""));
            m_a2_id.setText(prop.getProperty("anchor_2_id", ""));
            m_a2_x.setText (prop.getProperty("anchor_2_x", ""));
            m_a2_y.setText (prop.getProperty("anchor_2_y", ""));
            m_a2_z.setText (prop.getProperty("anchor_2_z", ""));
            m_a3_id.setText(prop.getProperty("anchor_3_id", ""));
            m_a3_x.setText (prop.getProperty("anchor_3_x", ""));
            m_a3_y.setText (prop.getProperty("anchor_3_y", ""));
            m_a3_z.setText (prop.getProperty("anchor_3_z", ""));
            m_a4_id.setText(prop.getProperty("anchor_4_id", ""));
            m_a4_x.setText (prop.getProperty("anchor_4_x", ""));
            m_a4_y.setText (prop.getProperty("anchor_4_y", ""));
            m_a4_z.setText (prop.getProperty("anchor_4_z", ""));
            m_a5_id.setText(prop.getProperty("anchor_5_id", ""));
            m_a5_x.setText (prop.getProperty("anchor_5_x", ""));
            m_a5_y.setText (prop.getProperty("anchor_5_y", ""));
            m_a5_z.setText (prop.getProperty("anchor_5_z", ""));
            m_a6_id.setText(prop.getProperty("anchor_6_id", ""));
            m_a6_x.setText (prop.getProperty("anchor_6_x", ""));
            m_a6_y.setText (prop.getProperty("anchor_6_y", ""));
            m_a6_z.setText (prop.getProperty("anchor_6_z", ""));
            m_a7_id.setText(prop.getProperty("anchor_7_id", ""));
            m_a7_x.setText (prop.getProperty("anchor_7_x", ""));
            m_a7_y.setText (prop.getProperty("anchor_7_y", ""));
            m_a7_z.setText (prop.getProperty("anchor_7_z", ""));
            m_a8_id.setText(prop.getProperty("anchor_8_id", ""));
            m_a8_x.setText (prop.getProperty("anchor_8_x", ""));
            m_a8_y.setText (prop.getProperty("anchor_8_y", ""));
            m_a8_z.setText (prop.getProperty("anchor_8_z", ""));

            m_log_pressure.setSelected(Boolean.valueOf(prop.getProperty("log_pressure", "false")));
            m_log_acceleration.setSelected(Boolean.valueOf(prop.getProperty("log_acceleration", "false")));
            m_log_magnetic.setSelected(Boolean.valueOf(prop.getProperty("log_magnetic", "false")));
            m_log_angular_velocity.setSelected(Boolean.valueOf(prop.getProperty("log_angular_velocity", "false")));
            m_log_euler_angles.setSelected(Boolean.valueOf(prop.getProperty("log_euler_angles", "false")));
            m_log_quaternion.setSelected(Boolean.valueOf(prop.getProperty("log_quaternion", "false")));
            m_log_linear_acceleration.setSelected(Boolean.valueOf(prop.getProperty("log_linear_acceleration", "false")));
            m_log_gravity.setSelected(Boolean.valueOf(prop.getProperty("log_gravity", "false")));

            m_position_smooth.getValueFactory().setValue(Integer.valueOf(prop.getProperty("position_smooth", "0")));
            m_velocity_smooth.getValueFactory().setValue(Integer.valueOf(prop.getProperty("velocity_smooth", "0")));

            m_use_file.setSelected(Boolean.valueOf(prop.getProperty("use_file", "false")));
            m_filename.setText(prop.getProperty("filename", ""));

            update_variables_from_gui();
        }
        catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private void refreshDisabledMobileIds() {
        m_mobile_device_1_id.setDisable(true);
        m_mobile_device_2_id.setDisable(true);
        m_mobile_device_3_id.setDisable(true);
        m_mobile_device_4_id.setDisable(true);
        m_mobile_device_5_id.setDisable(true);
        m_mobile_device_6_id.setDisable(true);

        number_mobile_devices = m_number_mobile_devices.getValue();

        switch (number_mobile_devices) {
            case "1":
                m_mobile_device_1_id.setDisable(false);
                break;
            case "2":
                m_mobile_device_1_id.setDisable(false);
                m_mobile_device_2_id.setDisable(false);
                break;
            case "3":
                m_mobile_device_1_id.setDisable(false);
                m_mobile_device_2_id.setDisable(false);
                m_mobile_device_3_id.setDisable(false);
                break;
            case "4":
                m_mobile_device_1_id.setDisable(false);
                m_mobile_device_2_id.setDisable(false);
                m_mobile_device_3_id.setDisable(false);
                m_mobile_device_4_id.setDisable(false);
                break;
            case "5":
                m_mobile_device_1_id.setDisable(false);
                m_mobile_device_2_id.setDisable(false);
                m_mobile_device_3_id.setDisable(false);
                m_mobile_device_4_id.setDisable(false);
                m_mobile_device_5_id.setDisable(false);
                break;
            case "6":
                m_mobile_device_1_id.setDisable(false);
                m_mobile_device_2_id.setDisable(false);
                m_mobile_device_3_id.setDisable(false);
                m_mobile_device_4_id.setDisable(false);
                m_mobile_device_5_id.setDisable(false);
                m_mobile_device_6_id.setDisable(false);
                break;
        }
    }

    private void refreshDisabledAnchors() {
        TextField[] anchor_5 = {m_a5_id, m_a5_x, m_a5_y, m_a5_z};
        TextField[] anchor_6 = {m_a6_id, m_a6_x, m_a6_y, m_a6_z};
        TextField[] anchor_7 = {m_a7_id, m_a7_x, m_a7_y, m_a7_z};
        TextField[] anchor_8 = {m_a8_id, m_a8_x, m_a8_y, m_a8_z};

        for (int i = 0; i < 4; i++) {
            anchor_5[i].setDisable(true);
            anchor_6[i].setDisable(true);
            anchor_7[i].setDisable(true);
            anchor_8[i].setDisable(true);
        }

        number_anchors = m_number_anchors.getValue();

        for (int i = 0; i < 4; i++) {
            switch (number_anchors) {
                case "4":
                    break;
                case "5":
                    anchor_5[i].setDisable(false);
                    break;
                case "6":
                    anchor_5[i].setDisable(false);
                    anchor_6[i].setDisable(false);
                    break;
                case "7":
                    anchor_5[i].setDisable(false);
                    anchor_6[i].setDisable(false);
                    anchor_7[i].setDisable(false);
                    break;
                case "8":
                    anchor_5[i].setDisable(false);
                    anchor_6[i].setDisable(false);
                    anchor_7[i].setDisable(false);
                    anchor_8[i].setDisable(false);
                    break;
            }
        }
    }

    private void refreshDisabledRangingAnchor() {
        update_variables_from_gui();
        if(Objects.equals(use_remote_1d_anchor, "false")) {
            m_range_anchor_id.setDisable(true);
        }
        else {
            m_range_anchor_id.setDisable(false);
        }
    }

    private void configureFileChooser(final FileChooser fileChooser) {
        fileChooser.setTitle("Save Settings Template");
        fileChooser.setInitialDirectory(
                new File(GetDocumentsFolder() + "Configurations/")
        );
        fileChooser.getExtensionFilters().add(
                new FileChooser.ExtensionFilter("Properties", "*.properties")
        );
    }

    void launchConsoleLogging(String executable, boolean showConsole, String[] args, String prependPathType) {
        try {
            stage = new Stage();
            FXMLLoader loader = new FXMLLoader(getClass().getClassLoader().getResource("fxml/console_window.fxml"));
            Parent root1 = loader.load();
            stage.setTitle("Console Output");
            stage.setScene(new Scene(root1));
            stage.setMaximized(false);
            //stage.initOwner(m_a1_id.getScene().getWindow());
            stage.initStyle(StageStyle.DECORATED);
            ConsoleWindow console_controller = loader.getController();
            stage.setOnCloseRequest(we -> console_controller.terminateProcess());
            if (showConsole) {
                stage.show();
            }

            console_controller.launchScript("Waiting for data to be collected...", executable, args, prependPathType);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    @Override
    public void initialize(URL location, ResourceBundle resources) {
        load_properties_from_file(GetDocumentsFolder() + "Configurations/MASTER_ACTIVE_CONFIG.properties");

        refreshDisabledMobileIds();
        m_number_mobile_devices.getSelectionModel().selectedItemProperty().addListener(
                (observableValue, oldStr, newStr) -> refreshDisabledMobileIds());

        refreshDisabledAnchors();
        m_number_anchors.getSelectionModel().selectedItemProperty().addListener(
                (observableValue, oldStr, newStr) -> refreshDisabledAnchors());

        refreshDisabledRangingAnchor();
        m_use_remote_1d_anchor.setOnAction((event -> {
            refreshDisabledRangingAnchor();
        }));

        TextFormatter<Integer> position_formatter = new TextFormatter<>(m_position_smooth.getValueFactory().getConverter(), m_position_smooth.getValueFactory().getValue());
        m_position_smooth.getEditor().setTextFormatter(position_formatter);
        m_position_smooth.getValueFactory().valueProperty().bindBidirectional(position_formatter.valueProperty());
        TextFormatter<Integer> velocity_formatter = new TextFormatter<>(m_position_smooth.getValueFactory().getConverter(), m_position_smooth.getValueFactory().getValue());
        m_velocity_smooth.getEditor().setTextFormatter(velocity_formatter);
        m_velocity_smooth.getValueFactory().valueProperty().bindBidirectional(velocity_formatter.valueProperty());
    }

    public void handleQuit() {
        Platform.exit();
    }

    public void handleConfigureUwbSettings() {
        Main main = new Main();
        main.openStage("fxml/configure_uwb_settings.fxml", "PSU Pozyx | UWB Settings", 800, 220);
    }

    public void handleDataReplay() {
        Main main = new Main();
        main.openStage("fxml/fxml/data_replay.fxml", "PSU Pozyx | Data Replay", 600, 400);
    }

    public void handleGraph2D(ActionEvent actionEvent) {
        saveSettingsForUse();
        launchConsoleLogging("graphing_realtime_2D", false, null,"PYINSTALLERPATH");
    }

    String GetDocumentsFolder() {
        String documentsFolder = FileSystemView.getFileSystemView().getDefaultDirectory().getPath() + "/PSUPozyx/";
        if(new SysTools().isMac()) {
            documentsFolder += "Library/Application Support/PSUPozyx/"; // may or may not work
        }
        return documentsFolder;
    }

    String TraverseUpToRootFolder() {
        try {
            String currentLocation = getClass().getProtectionDomain().getCodeSource().getLocation().toURI().getPath();
            currentLocation = currentLocation.substring(0, currentLocation.lastIndexOf("target"));
            return currentLocation;
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
        return "";
    }
}


