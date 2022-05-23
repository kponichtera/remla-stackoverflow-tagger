import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {InferenceFormComponent} from "./inference-form.component";
import {MatButtonModule} from "@angular/material/button";
import {MatChipsModule} from "@angular/material/chips";
import {MatInputModule} from "@angular/material/input";
import {TagsInputComponent} from './components/tags-input/tags-input.component';
import {MatIconModule} from "@angular/material/icon";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatSnackBarModule} from "@angular/material/snack-bar";


@NgModule({
  imports: [
    CommonModule,
    MatButtonModule,
    MatChipsModule,
    MatInputModule,
    MatIconModule,
    ReactiveFormsModule,
    FormsModule,
    MatSnackBarModule
  ],
  declarations: [
    InferenceFormComponent,
    TagsInputComponent
  ],
  exports: [
    InferenceFormComponent
  ]
})
export class InferenceFormModule { }
