import {Component} from '@angular/core';
import {MatSnackBar} from "@angular/material/snack-bar";
import {CorrectionRequest, InferenceService, PredictionRequest} from "../../services/inference.service";

@Component({
  selector: 'app-inference-form',
  templateUrl: './inference-form.component.html',
  styleUrls: ['./inference-form.component.scss']
})
export class InferenceFormComponent  {

  title: string = '';
  tags: string[] = [];
  newTag: string = '';

  processedTitle: string = '';
  predictedTags: string[] = [];

  constructor(private _snackBar: MatSnackBar,
              private _inferenceService: InferenceService) {
  }

  query(): void {
    if (this.title.trim() === '') {
      this._snackBar.open('Title is missing!', 'Close', {duration: 3000})
      return;
    }

    let request: PredictionRequest = {
      title: this.title
    }

    this._inferenceService.predict(request).subscribe({
      next: response => {
        this.processedTitle = response.title;
        this.predictedTags = response.tags;
        this.tags = response.tags;
      },
      error: _ => {
        this._snackBar.open('Error has occurred', 'Close', {duration: 3000})
      }
    });

  }

  submitFeedback() {
    let request: CorrectionRequest = {
      title: this.processedTitle,
      predicted: this.predictedTags,
      actual: this.tags
    }
    this._inferenceService.correctPrediction(request).subscribe({
      next: _ => {
        this._snackBar.open('Thank you!', 'Close', {duration: 3000});
        this.reset()
      },
      error: _ => {
        this._snackBar.open('Error has occurred', 'Close', {duration: 3000})
      }
    });
  }

  reset() {
    this.title = '';
    this.newTag = '';
    this.processedTitle = '';
    this.tags = [];
    this.predictedTags = [];
  }

}
