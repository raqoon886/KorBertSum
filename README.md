# BertSum

**This code is from paper `Fine-tune BERT for Extractive Summarization`**(https://arxiv.org/pdf/1903.10318.pdf)

**!New: Please see our [full paper](https://arxiv.org/abs/1908.08345) with trained models**

Package Requirements: pytorch pytorch_pretrained_bert tensorboardX multiprocess pyrouge

Some codes are borrowed from ONMT(https://github.com/OpenNMT/OpenNMT-py)

## 한국어 문서 추출요약을 위한 Modified BertSum

### 해당 문서의 원저작권은 Nlpyang의 [BertSum](https://github.com/nlpyang/BertSum) 에 있습니다.

### **[저의 벨로그](https://velog.io/@raqoon886/KorBertSum-SummaryBot)** 에 코드와 플로우 설명이 있습니다.


#### Step 1. Prepare Data

To run etri-api-scraper.py
```
python etri_api_scraper.py --input '.../train.jsonl' --api_key 'openapi key' --first_index 0 --last_index 5000
```

From newsdata to json
```
python article_to_json.py -mode train -news_dir '' -output ''
```

From json to Bert pytorch file
```
python preprocess.py -mode format_to_bert -raw_path ../json_data -save_path ../bert_data -vocab_file_path 'etri vocab file list'
```

#### Step 2. Train

To train with endoer-classifier
```
python train.py -mode train -encoder classifier -dropout 0.1 -bert_data_path ../bert_data/korean -model_path ../models/bert_classifier -lr 2e-3 -visible_gpus 0 -gpu_ranks 0 -world_size 1 -report_every 50 -save_checkpoint_steps 1000 -batch_size 1000 -decay_method noam -train_steps 1000 -accum_count 1 -log_file ../logs/bert_classifier -use_interval true -warmup_steps 8000 -bert_model ../001_bert_morp_pytorch -bert_config_path ../001_bert_morp_pytorch/bert_config.json -temp_dir ../temp
```

#### Step 3. Validate

위의 코드에서 -mode validate로 수정하면 됩니다.

#### Step 4. Test

위의 코드에서 -mode test -test_from bert_model_path 로 수정하면 됩니다.

실행 예시 파일 Newsdata_extractive_summ.ipynb 에 실행 예시가 있습니다.


## CHATBOT

Newsdata_summarybot.ipynb 에 실행 예시가 있습니다.
![example](https://github.com/raqoon886/KoBertSum/tree/master/summbot.png)

