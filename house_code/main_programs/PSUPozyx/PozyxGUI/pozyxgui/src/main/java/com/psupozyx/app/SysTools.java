package com.psupozyx.app;

public class SysTools {
    private String OS = System.getProperty("os.name").toLowerCase();

    boolean isWindows() {
        return (OS.contains("win"));
    }

    boolean isMac() {
        return (OS.contains("mac"));
    }

    boolean isUnix() {
        return (OS.contains("nix") || OS.contains("nux") || OS.indexOf("aix") > 0 );
    }

    boolean isSolaris() {
        return (OS.contains("sunos"));
    }
}
