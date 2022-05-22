import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {HomepageRoutingModule} from './homepage-routing.module';
import {HomepageComponent} from './homepage.component';
import {InferenceFormModule} from "../../components/inference-form/inference-form.module";
import {MatCardModule} from "@angular/material/card";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {HttpClientModule} from "@angular/common/http";
import {MatIconModule} from "@angular/material/icon";


@NgModule({
  declarations: [
    HomepageComponent
  ],
  imports: [
    CommonModule,
    HomepageRoutingModule,
    InferenceFormModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatIconModule
  ]
})
export class HomepageModule { }
