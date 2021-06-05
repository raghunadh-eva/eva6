Name: Raghunadh Puranam

Email: raghunadpuranam@gmail.com

Assignment 5 EVA6: Accuracy 99.4% consistently , < 15 Epochs , < 10000 parameters

CODE1:

Implement the setting up part of the code (without simply doing CTRL+C and CTRL+V :) ) for practice

Visualize the input data with & without normalization - This is an extra piece which I'll leave commented

I have also started with the GAP as standard and hence added it at the beginning

**Target**

  1. Start with lightest model possible for the objective

        	1. BLOCK1: 28x28x1 | 3x3x1x16 -> 26x26x16 | 3x3x16x32 --> 24x24x32
                	2. TRANSITION BLOCK: 24x24x32 | 1x1x32x10 -> 24x24x10 | MaxPool(2d) -> 12x12x10
                        	3. BLOCK2: 12x12x10 | 3x3x10x16 -> 10x10x16 | 3x3x16 -> 8x8x16
                                	4. OUTPUT BLOCK: 8x8x16 | AvgPool2d(8)  | 1x1x16x10 

  2. Use batch normalization after every layer except the last one

  3. The train and test were following each other until EPOCH: 8 and  it shows signs of over-fitting and finally at EPOCH:14 I have delta of 0.5%

  4. ```
     EPOCH: 9
     Loss=0.05103536322712898 Batch_id=468 Accuracy=99.10: 100%|██████████| 469/469 [00:16<00:00, 28.37it/s]
       0%|          | 0/469 [00:00<?, ?it/s]
     Test set: Average loss: 0.0396, Accuracy: 9887/10000 (98.87%)
     
     EPOCH: 10
     Loss=0.016225555911660194 Batch_id=468 Accuracy=99.16: 100%|██████████| 469/469 [00:16<00:00, 28.35it/s]
       0%|          | 0/469 [00:00<?, ?it/s]
     Test set: Average loss: 0.0376, Accuracy: 9902/10000 (99.02%)
     
     EPOCH: 11
     Loss=0.023538747802376747 Batch_id=468 Accuracy=99.22: 100%|██████████| 469/469 [00:16<00:00, 28.22it/s]
       0%|          | 0/469 [00:00<?, ?it/s]
     Test set: Average loss: 0.0320, Accuracy: 9905/10000 (99.05%)
     
     EPOCH: 12
     Loss=0.009567794390022755 Batch_id=468 Accuracy=99.24: 100%|██████████| 469/469 [00:16<00:00, 28.49it/s]
       0%|          | 0/469 [00:00<?, ?it/s]
     Test set: Average loss: 0.0289, Accuracy: 9913/10000 (99.13%)
     
     EPOCH: 13
     Loss=0.026352807879447937 Batch_id=468 Accuracy=99.27: 100%|██████████| 469/469 [00:16<00:00, 28.44it/s]
       0%|          | 0/469 [00:00<?, ?it/s]
     Test set: Average loss: 0.0331, Accuracy: 9900/10000 (99.00%)
     
     EPOCH: 14
     Loss=0.03931316360831261 Batch_id=468 Accuracy=99.39: 100%|██████████| 469/469 [00:16<00:00, 28.07it/s]
     Test set: Average loss: 0.0363, Accuracy: 9892/10000 (98.92%)
     ```

  5. Results

        	11. 9136 parameters , 15 epochs
        2. Best train: 99.39 (epoch15)
        3. Best test: 99.13 (epoch13)

 	6. Analysis:

      	1. Good model to start with. Lesser size
      	2. Need to improve the model - but need to address the over-fitting

  7. Next steps:

        	1. Add dropOut




<u>**CODE2:**</u> Same as above/below block, except added dropOut of 5% after every layer (except the final/transition layer)

BLOCK1: 28x28x1 | 3x3x1x16 -> 26x26x16 | 3x3x16x32 --> 24x24x32

TRANSITION BLOCK: 24x24x32 | 1x1x32x10 -> 24x24x10 | MaxPool(2d) -> 12x12x10

BLOCK2: 12x12x10 | 3x3x10x16 -> 10x10x16 | 3x3x16 -> 8x8x16

OUTPUT BLOCK: 8x8x16 | AvgPool2d(8)  | 1x1x16x10

**<u>Explanation</u>**

The accuracy in the first EPOCH dropped after adding dropOut

```
Loss=0.17522762715816498 Batch_id=468 Accuracy=81.09: 100%|██████████| 469/469 [00:10<00:00, 44.71it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.1467, Accuracy: 9670/10000 (96.70%)
```

However , the gap between train and test accuracy has reduced. Now that's sign of good model for us as discussed in the class. Results of last few epochs.

Only big difference occurred in the last epoch which is of 0.23% , other than that the train and test were closely following 

```
EPOCH: 10
Loss=0.02929815463721752 Batch_id=468 Accuracy=98.88: 100%|██████████| 469/469 [00:10<00:00, 43.14it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0341, Accuracy: 9889/10000 (98.89%)

EPOCH: 11
Loss=0.060033876448869705 Batch_id=468 Accuracy=98.87: 100%|██████████| 469/469 [00:10<00:00, 43.33it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0395, Accuracy: 9872/10000 (98.72%)

EPOCH: 12
Loss=0.08610863238573074 Batch_id=468 Accuracy=98.94: 100%|██████████| 469/469 [00:11<00:00, 42.56it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0355, Accuracy: 9891/10000 (98.91%)

EPOCH: 13
Loss=0.02014150470495224 Batch_id=468 Accuracy=98.93: 100%|██████████| 469/469 [00:10<00:00, 43.63it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0328, Accuracy: 9895/10000 (98.95%)

EPOCH: 14
Loss=0.024509109556674957 Batch_id=468 Accuracy=98.97: 100%|██████████| 469/469 [00:11<00:00, 42.49it/s]
Test set: Average loss: 0.0380, Accuracy: 9875/10000 (98.75%)
```

  1. Results

     1. 9136 parameters , 15 epochs
     2. Best train: 98.94 (epoch12)
     3. Best test: 98.95 (epoch13)

  2. Analysis:

     	1. Good model to start with. Lesser size
     	2. Over fitting is addressed
     	3. Need to improve the model for improving the accuracy
     	4. There is 1.03% scope to improve in training which can be transferred to test

  3. Next steps:

         1. The next silver bullet is to introduce variety into the model by using augmentation,so that it can see same data but with different
         2. Looking at the input data for MNIST the values are zeros on the periphery & mean was close to zero as well, hence decided to use augmentation by filling 0's when rotated



<u>**CODE3:**</u> Same as above/below block + added image rotation of 7% by filling 0's

BLOCK1: 28x28x1 | 3x3x1x16 -> 26x26x16 | 3x3x16x32 --> 24x24x32

TRANSITION BLOCK: 24x24x32 | 1x1x32x10 -> 24x24x10 | MaxPool(2d) -> 12x12x10

BLOCK2: 12x12x10 | 3x3x10x16 -> 10x10x16 | 3x3x16 -> 8x8x16

OUTPUT BLOCK: 8x8x16 | AvgPool2d(8)  | 1x1x16x10

**<u>Explanation</u>** There was never once in the logs , where train beats test across all the epochs.

But the accuracy of train has reduced when compared to the previous model. When comparing the EPOCHS between the previous and this one,

the training accuracy has reduced but performance in test improved across all the epochs. This indicates that the model should learn more basically it 

boils down to capacity.

```
EPOCH: 10
Loss=0.07593976706266403 Batch_id=468 Accuracy=98.54: 100%|██████████| 469/469 [00:23<00:00, 19.90it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0396, Accuracy: 9868/10000 (98.68%)

EPOCH: 11
Loss=0.11675160378217697 Batch_id=468 Accuracy=98.60: 100%|██████████| 469/469 [00:23<00:00, 19.80it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0339, Accuracy: 9892/10000 (98.92%)

EPOCH: 12
Loss=0.07936053723096848 Batch_id=468 Accuracy=98.63: 100%|██████████| 469/469 [00:23<00:00, 19.88it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0338, Accuracy: 9891/10000 (98.91%)

EPOCH: 13
Loss=0.047473084181547165 Batch_id=468 Accuracy=98.66: 100%|██████████| 469/469 [00:23<00:00, 19.95it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0350, Accuracy: 9878/10000 (98.78%)

EPOCH: 14
Loss=0.008319215849041939 Batch_id=468 Accuracy=98.66: 100%|██████████| 469/469 [00:23<00:00, 19.92it/s]
Test set: Average loss: 0.0372, Accuracy: 9887/10000 (98.87%)
```

  1. Results

     1. 9136 parameters , 15 epochs
     2. Best train: 98.94
     3. Best test: 98.92

  2. Analysis:

     	1. Good model to start with. Lesser size
     	2. Over fitting is addressed
     	3. Image rotation improved test accuracy by hitting that in early epochs, but train accuray has stagnated

  3. Next steps:

         1. Should improve the capacity

**<u>CODE4:</u>**



BLOCK1: 28x28x1 | 3x3x1x10 -> 26x26x10 | 3x3x10x18 --> 24x24x18

TRANSITION BLOCK: 24x24x18 | 1x1x18x10 -> 24x24x10 | MaxPool(2d) -> 12x12x10

BLOCK2: 12x12x10 | 3x3x10x16 -> 10x10x16 | 3x3x20 -> 8x8x16x20

TRANSITION BLOCK: 8x8x20 | 1x1x20x10 -> 8x8x10

BLOCK3: 8x8x10 | 3x3x32 -> 6x6x32

OUTPUT BLOCK: 6x6x32 | AvgPool2d(6)  | 1x1x32x10

**Explanation:** The changes were to reduce the kernel size in block 1 ,so that we can increase the capacity in the second layer

Added one more transition block and increased the output kernels at the final layer before GAP , followed by 1x1

```
EPOCH: 10
Loss=0.033552903681993484 Batch_id=468 Accuracy=99.02: 100%|██████████| 469/469 [00:23<00:00, 19.85it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0226, Accuracy: 9934/10000 (99.34%)

EPOCH: 11
Loss=0.017199618741869926 Batch_id=468 Accuracy=99.09: 100%|██████████| 469/469 [00:23<00:00, 19.83it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0214, Accuracy: 9935/10000 (99.35%)

EPOCH: 12
Loss=0.005722430068999529 Batch_id=468 Accuracy=99.05: 100%|██████████| 469/469 [00:23<00:00, 19.71it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0214, Accuracy: 9936/10000 (99.36%)

EPOCH: 13
Loss=0.011901051737368107 Batch_id=468 Accuracy=99.11: 100%|██████████| 469/469 [00:23<00:00, 19.62it/s]
  0%|          | 0/469 [00:00<?, ?it/s]
Test set: Average loss: 0.0189, Accuracy: 9938/10000 (99.38%)

EPOCH: 14
Loss=0.024716340005397797 Batch_id=468 Accuracy=99.06: 100%|██████████| 469/469 [00:23<00:00, 19.85it/s]
Test set: Average loss: 0.0222, Accuracy: 9935/10000 (99.35%)
```

    1. Results

       1. 9802 parameters , 15 epochs
       2. Best train: 99.11
       3. Best test: 99.38
    2. Analysis - No overfitting , slightly bigger model hitting consistent accuracy
           1. Still possibility of improving the training accuracy , but will increase parameters.
           2. Need method to contain the parameters , yet increase accuracy.
           3. Will continue to work