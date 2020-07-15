package in.celph.gtpro;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategy;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import org.apache.commons.collections4.MapUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.traccar.model.Position;

import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;
import java.util.Objects;

@JsonNaming(PropertyNamingStrategy.SnakeCaseStrategy.class)
public final class GpsEvent implements Serializable {
    private static final Logger LOGGER = LoggerFactory.getLogger(GpsEvent.class);
    private final String imeiNo;
    private final String lattitude;
    private final String longitude;
    private final String lattitudeDirection;
    private final String longitudeDirection;
    private final String speed;
    private final String digitalPort1;
    private final String digitalPort2;
    private final String digitalPort3;
    private final String digitalPort4;
    private final String analogPort1;
    private final String analogPort2;
    private final String angle;
    private final String satellite;
    private final String time;
    private final String batteryVoltage;
    private final String gpsValidity;

    public GpsEvent(final String imeiNo, final Position position) {
        this.imeiNo = imeiNo;
        this.lattitude = String.valueOf(position.getLatitude());;
        this.longitude = String.valueOf(position.getLongitude());
        this.lattitudeDirection = "N";
        this.longitudeDirection = "E";
        this.speed = String.valueOf(position.getSpeed());
        this.digitalPort1 = "0";
        this.digitalPort2 = "0";
        this.digitalPort3 = "0";
        this.digitalPort4 = "0";
        this.analogPort1 = "0";
        this.analogPort2 = "0";
        this.angle = "0";
        this.satellite = "0";
        this.time = formatGpsTime(String.valueOf(position.getFixTime().getTime()));
        this.batteryVoltage = getBatteryValue(position.getAttributes());;
        this.gpsValidity = "A";
    }

    public String getImeiNo() {
        return imeiNo;
    }

    public String getLattitude() {
        return lattitude;
    }

    public String getLongitude() {
        return longitude;
    }

    public String getLattitudeDirection() {
        return lattitudeDirection;
    }

    public String getLongitudeDirection() {
        return longitudeDirection;
    }

    public String getSpeed() {
        return speed;
    }

    public String getDigitalPort1() {
        return digitalPort1;
    }

    public String getDigitalPort2() {
        return digitalPort2;
    }

    public String getDigitalPort3() {
        return digitalPort3;
    }

    public String getDigitalPort4() {
        return digitalPort4;
    }

    public String getAnalogPort1() {
        return analogPort1;
    }

    public String getAnalogPort2() {
        return analogPort2;
    }

    public String getAngle() {
        return angle;
    }

    public String getSatellite() {
        return satellite;
    }

    public String getTime() {
        return time;
    }

    public String getBatteryVoltage() {
        return batteryVoltage;
    }

    public String getGpsValidity() {
        return gpsValidity;
    }

    private String getBatteryValue(Map<String, Object> map){
        final String defVal = "0.0";
        if(MapUtils.isEmpty(map)){
            return defVal;
        }

        if(Objects.isNull(map.get("battery"))){
            return defVal;
        }

        return String.valueOf(map.get("battery"));
    }

    private String formatGpsTime(final String timeInSeconds){
        final String expectedFormat = "yyyy-MM-dd HH:mm:ss";
        LOGGER.info("formatGpsTime | timeInSeconds: {}, expectedFormat: {}",timeInSeconds, expectedFormat);
        Long timeInMills = Long.valueOf(timeInSeconds) * 1000;
        LOGGER.info("formatGpsTime | timeInMills: {}, expectedFormat: {}",timeInMills, expectedFormat);
        Date date = new Date(timeInMills);
        SimpleDateFormat formatter = new SimpleDateFormat(expectedFormat);
        return formatter.format(date);
    }

    public static GpsEvent getInstance(final String imeiNo, final Position position){
        return new GpsEvent(imeiNo, position);
    }
}
