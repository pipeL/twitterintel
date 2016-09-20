from kafkaconsumer import KafkaConsumerSpout

from worddivider import WordDividerBolt
from twoworddivider import TwoWordDividerBolt
from threeworddivider import ThreeWordDividerBolt

from twowordcount import TwoWordCountBolt
from threewordcount import ThreeWordCountBolt
from wordcount import WordCountBolt

def create(builder):
    builder.setSpout("KafkaConsumer", KafkaConsumerSpout(),1)
    builder.setBolt("WordDivider", WordDividerBolt(),1).shuffleGrouping("KafkaConsumer")
    builder.setBolt("TwoWordDivider", TwoWordDividerBolt(),1).shuffleGrouping("KafkaConsumer")
    builder.setBolt("ThreeWordDivider", ThreeWordDividerBolt(),1).shuffleGrouping("KafkaConsumer")
    builder.setBolt("CountWord", WordCountBolt(),2).fieldsGrouping("WordDivider",["word"])
    builder.setBolt("CountTwoWords", TwoWordCountBolt(),2).fieldsGrouping("TwoWordDivider",["word"])
    builder.setBolt("CountThreeWords", ThreeWordCountBolt(),2).fieldsGrouping("ThreeWordDivider",["word"])
