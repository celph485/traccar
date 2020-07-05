package in.celph.gtpro;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

final class ConfigBuilder {

    private static final Logger LOGGER = LoggerFactory.getLogger(ConfigBuilder.class);

    static final String MQ_HOST = "mq-host";
    static final String MQ_PORT = "mq-port";
    static final String MQ_USER = "mq-user";
    static final String MQ_PASS = "mq-pass";
    static final String MQ_DESTINATION = "mq-destination";

    private final String configFileLoc;
    private final String mappingFileLoc;
    private final Map<String, String> configMap;
    private final Map<Long, String> deviceMap;

    private ConfigBuilder() throws IOException {
        LOGGER.info("Creating instance of ConfigBuilder");
        configFileLoc = "/opt/traccar/conf/config.properties";
        LOGGER.info("configFileLoc: "+configFileLoc);
        mappingFileLoc = "/opt/traccar/conf/mapping.properties";
        LOGGER.info("mappingFileLoc: "+mappingFileLoc);
        this.configMap = populateConfigMap();
        this.deviceMap = populateDeviceMap();
    }

    static ConfigBuilder getInstance() throws IOException {
        return new ConfigBuilder();
    }

    Map<Long, String> getDeviceMap() {
        return deviceMap;
    }

    Map<String, String> getConfigMap() {
        return configMap;
    }

    private Map<Long, String> populateDeviceMap() throws IOException {
        LOGGER.info("Populating device-imei mapping");
        Map<Long, String> map = new HashMap<>();
        Properties prop = getProperties(mappingFileLoc);
        for(String key: prop.stringPropertyNames()){
            final String val = prop.getProperty(key);
            map.put(Long.valueOf(key), val);
        }
        return Collections.unmodifiableMap(map);
    }

    private Map<String, String> populateConfigMap() throws IOException {
        LOGGER.info("Populating config map");
        Map<String, String> map = new HashMap<>();
        Properties prop = getProperties(configFileLoc);
        map.put(MQ_HOST, prop.getProperty(MQ_HOST));
        map.put(MQ_PORT, prop.getProperty(MQ_PORT));
        map.put(MQ_USER, prop.getProperty(MQ_USER));
        map.put(MQ_PASS, prop.getProperty(MQ_PASS));
        map.put(MQ_DESTINATION, prop.getProperty(MQ_DESTINATION));

        for(Map.Entry<String, String> entry : map.entrySet()){
            final String key = entry.getKey();
            final String val = entry.getValue();
            if(StringUtils.isEmpty(val))
                throw new IllegalArgumentException("Empty value for "+key+" in config file");
        }

        return Collections.unmodifiableMap(map);
    }

    private Properties getProperties(final String filePath) throws IOException {
        LOGGER.info("Loading properties from " + filePath);
        try(InputStream inputStream = new FileInputStream(filePath)){
            Properties prop = new Properties();
            prop.load(inputStream);
            return prop;
        }
    }
}
