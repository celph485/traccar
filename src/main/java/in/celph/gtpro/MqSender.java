package in.celph.gtpro;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.traccar.model.Position;

import javax.jms.*;
import java.util.Map;

public class MqSender {
    private static final Logger LOGGER = LoggerFactory.getLogger(MqSender.class);
    private Map<String, String> configMap;
    private Map<Long, String> deviceMap;
    private boolean canSend;
    private MqSender(){
        LOGGER.info("Creating instance of MqSender");
        try {
            ConfigBuilder configBuilder = ConfigBuilder.getInstance();
            configMap = configBuilder.getConfigMap();
            deviceMap = configBuilder.getDeviceMap();
            canSend = Boolean.TRUE;
        } catch (Exception e) {
            LOGGER.error("Won't be able to send data to MQ",e);
            canSend = Boolean.FALSE;
        }
    }

    public static MqSender getInstance(){
        return Holder.INSTANCE;
    }

    private static class Holder{
        private static final MqSender INSTANCE = new MqSender();
    }

    public boolean send(final Position position){
        if(!canSend){
            LOGGER.warn("Can not sent to MQ due to config issue");
            return false;
        }
        final String imei = deviceMap.get(position.getDeviceId());

        if(StringUtils.isEmpty(imei)){
            LOGGER.warn("Device id "+position.getDeviceId() + " is not whitelisted for MQ");
            return false;
        }

        final String data = getJsonFormatData(GpsEvent.getInstance(imei, position));

        if(StringUtils.isEmpty(data)){
            LOGGER.warn("Won't be able to send data to MQ for device id: {}, please check logs. ",position.getDeviceId());
            return false;
        }
        return sendDataToMq(data);
    }

    private boolean sendDataToMq(final String data){
        LOGGER.info("sending data to MQ: {}", data);
        try{
            final String queueName = configMap.get(ConfigBuilder.MQ_DESTINATION);
            final String mqAddr = "tcp://"
                    +configMap.get(ConfigBuilder.MQ_HOST)
                    +":"
                    +configMap.get(ConfigBuilder.MQ_PORT);
            ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory(mqAddr);
            Connection connection = connectionFactory.createConnection();
            connection.start();
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            Destination destination = session.createQueue(queueName);
            MessageProducer producer = session.createProducer(destination);
            producer.setDeliveryMode(DeliveryMode.PERSISTENT);
            TextMessage message = session.createTextMessage(data);
            producer.send(message);
            session.close();
            connection.close();
            LOGGER.info("Sent to MQ.");
            return true;
        }catch (Exception e){
            LOGGER.error("Error while sending position to mq", e);
            return false;
        }
    }

    private String getJsonFormatData(final GpsEvent gpsEvent){
        ObjectMapper mapper = new ObjectMapper();
        try {
            return mapper.writeValueAsString(gpsEvent);
        } catch (JsonProcessingException e) {
            LOGGER.error("Unable to create json string ", e);
            return StringUtils.EMPTY;
        }
    }
}
